from abc import ABC
from dataclasses import dataclass, field
from typing import Self

from klaatu_python.utils import partition, zip_dict_lists

from zoho.records.base import AbstractIDRecord
from zoho.records.tag import Tag as ZohoTag
from zoho.requestor import ZohoRequestor
from zoho.search import Search
from zoho.settings import settings


@dataclass
class AbstractModuleRecord(AbstractIDRecord, ABC):
    module: str

    @classmethod
    def _get_api_url(cls):
        return f"{ZohoRequestor.singleton().token.api_domain}/crm/v5/{cls.module}"

    @classmethod
    def bulk_update(cls, records: list[Self]) -> list[Self]:
        results: list[Self] = []
        idx = 0

        for partial_data in partition(records, 100):
            json = {"data": [d.to_dict() for d in partial_data]}
            try:
                response = ZohoRequestor.singleton().put(url=cls._get_api_url(), json=json)
                for row in response.get("data", []):
                    if "details" in row and "id" in row["details"]:
                        results.append(records[idx].with_id(row["details"]["id"]))
                    else:
                        results.append(records[idx])
                    idx += 1
            except Exception as e:
                print(f"!!! Error: {e}")

        return results

    @classmethod
    def bulk_upsert(cls, records: list[Self]) -> list[Self]:
        results: list[Self] = []
        idx = 0

        for partial_data in partition(records, 100):
            response = ZohoRequestor.singleton().post(
                url=f"{cls._get_api_url()}/upsert",
                json={"data": [d.to_dict() for d in partial_data]},
            )
            for row in response.get("data", []):
                if "details" in row and "id" in row["details"]:
                    results.append(records[idx].with_id(row["details"]["id"]))
                idx += 1

        return results

    @classmethod
    def get(cls, record_id: str) -> Self | None:
        response = ZohoRequestor.singleton().get(url=f"{cls._get_api_url()}/{record_id}")
        if "data" in response and response["data"]:
            return cls.from_dict(response["data"][0])
        return None

    @classmethod
    def list(
        cls,
        fields: list[str] | None = None,
        limit: int | None = None,
        search: Search | None = None,
        **kwargs,
    ) -> list[Self]:
        """
        @param kwargs Values that are lists will be searched for using the "in"
        operator, all others with "equals".
        """
        limit = limit or settings.list_limit
        per_page = limit if limit and limit < 200 else 200
        fields = fields or cls.dict_keys()
        records = []

        if kwargs:
            eq_kwargs = {k: v for k, v in kwargs.items() if not isinstance(v, list)}
            in_kwargs = {k: v for k, v in kwargs.items() if isinstance(v, list)}
            search = search or Search()
            if eq_kwargs:
                search = search.eq(**eq_kwargs)
            if in_kwargs:
                search = search.in_(**in_kwargs)

        if search:
            url = f"{cls._get_api_url()}/search?criteria={search()}"
        else:
            url = cls._get_api_url()

        for field_list in partition(fields, 50):
            records.append(
                ZohoRequestor.singleton().get_list(
                    url=url,
                    get_params={"fields": ",".join(field_list)},
                    list_field="data",
                    limit=limit,
                    per_page=per_page,
                )
            )

        return [cls.from_dict(row) for row in zip_dict_lists(records)]

    def update(self):
        ZohoRequestor.singleton().put(url=self._get_api_url(), json={"data": [self.to_dict()]})


@dataclass
class AbstractTaggedModuleRecord(AbstractModuleRecord, ABC):
    Tag: list[ZohoTag] = field(default_factory=list)

    @classmethod
    def bulk_tag(cls, objs: list[Self], tags: list[ZohoTag]) -> list[Self]:
        untagged_objs = [obj for obj in objs if set(tags) - set(obj.Tag)]
        tagged_objs = list(set(objs) - set(untagged_objs))
        data = [
            {
                "id": obj.id,
                "Tag": [tag.to_dict() for tag in set(obj.Tag).union(tags)],
            }
            for obj in untagged_objs
        ]
        for partial in partition(data, 100):
            ZohoRequestor.singleton().put(url=cls._get_api_url(), json={"data": partial})
        tagged_objs.extend(obj.copy(Tag=list(set(obj.Tag).union(tags))) for obj in untagged_objs)
        return tagged_objs
