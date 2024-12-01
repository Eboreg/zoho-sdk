from dataclasses import dataclass
from typing import List, Self

from klaatu_python.utils import getitem0_nullable

from zoho.records.base import AbstractIDRecord
from zoho.requestor import ZohoRequestor
from zoho.types import ColorCode


@dataclass
class Tag(AbstractIDRecord):
    name: str
    color_code: ColorCode | None = None

    def __hash__(self) -> int:
        return hash((self.id, self.name, self.color_code))

    @classmethod
    def _get_api_url(cls, module: str):
        return f"{ZohoRequestor.singleton().token.api_domain}/crm/v5/settings/tags?module={module}"

    @classmethod
    def bulk_create(cls, module: str, tags: list[Self]) -> list[Self]:
        response = ZohoRequestor.singleton().post(
            url=cls._get_api_url(module),
            json={"tags": [t.to_dict() for t in tags]},
        )
        created: list[Tag] = []

        for idx, row in enumerate(response.get("tags", [])):
            tag_id = row.get("details", {}).get("id", None)
            if tag_id:
                created.append(
                    Tag(
                        id=tag_id,
                        name=tags[idx].name,
                        color_code=tags[idx].color_code,
                    )
                )

        return created

    @classmethod
    def get(cls, module: str, name: str) -> Self | None:
        return getitem0_nullable(cls.list(module), cond=lambda t: t.name == name)

    @classmethod
    def get_or_create(cls, module: str, name: str, default_color_code: ColorCode = "#658BA8") -> Self:
        return cls.list_or_create(module, [name], default_color_code)[0]

    @classmethod
    def list(cls, module: str) -> list[Self]:
        return [
            cls.from_dict(row)
            for row in ZohoRequestor.singleton().get_list(url=cls._get_api_url(module), list_field="tags")
        ]

    @classmethod
    def list_or_create(cls, module: str, names: List[str], default_color_code: ColorCode = "#658BA8") -> List[Self]:
        tags = [t for t in cls.list(module) if t.name in names]
        missing_names = [n for n in names if n not in [tag.name for tag in tags]]

        if missing_names:
            unsaved_tags = [Tag(id=None, name=name, color_code=default_color_code) for name in missing_names]
            tags.extend(cls.bulk_create(module, unsaved_tags))

        return tags
