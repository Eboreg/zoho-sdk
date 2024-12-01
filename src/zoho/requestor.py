import logging
from enum import Enum
from typing import Self
from urllib.parse import urlencode

import requests

from zoho.exceptions import ZohoHTTPError
from zoho.oauth2 import (
    ZohoOAuth2Token,
    get_oauth2_token_from_auth_code,
    get_oauth2_token_from_refresh_token,
)
from zoho.settings import settings
from zoho.utils import now


logger = logging.getLogger(__name__)


class HTTPMetod(Enum):
    GET = "get"
    POST = "post"
    DELETE = "delete"
    PUT = "put"


class ZohoRequestor:
    auth_url: str = "https://accounts.zoho.eu/oauth/v2/token"
    _token: ZohoOAuth2Token
    _instance: Self

    @property
    def token(self) -> ZohoOAuth2Token:
        if not hasattr(self, "_token") or self._token.expires < now():
            if not settings.client_id or not settings.client_secret:
                raise ValueError("settings.client_id and settings.client_secret must be set.")
            if settings.refresh_token:
                self._token = get_oauth2_token_from_refresh_token(settings.refresh_token)
            elif settings.auth_code:
                self._token = get_oauth2_token_from_auth_code(settings.auth_code)
            else:
                raise ValueError("settings.refresh_token or settings.auth_code must be set.")

        return self._token

    @classmethod
    def singleton(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def delete(self, url: str) -> dict:
        return self.request(url=url, method=HTTPMetod.DELETE)

    def get(self, url: str) -> dict:
        return self.request(url=url, method=HTTPMetod.GET)

    def get_list(
        self,
        url: str,
        list_field: str,
        get_params: dict | None = None,
        per_page: int | None = None,
        limit: int | None = None,
        use_page_tokens: bool = True,
    ) -> list[dict]:
        limit = limit or settings.list_limit
        more_items = True
        next_page_token = None
        page = 1
        base_url = url
        base_get_params = (get_params or {}).copy()
        items = []

        while more_items:
            final_get_params = base_get_params.copy()
            if next_page_token and use_page_tokens:
                final_get_params["page_token"] = next_page_token
            else:
                if per_page:
                    final_get_params["per_page"] = per_page
                final_get_params["page"] = page
            url = base_url
            if final_get_params:
                if "?" in url:
                    url += "&"
                else:
                    url += "?"
                url += urlencode(final_get_params, safe=',')
            response = self.get(url=url)
            items.extend(response.get(list_field, []))
            info = response.get("info", {})
            more_items = info.get("more_records", False) and (limit is None or len(items) < limit)
            next_page_token = info.get("next_page_token", None)
            page += 1

        return items

    def post(self, url: str, json: dict | None = None) -> dict:
        return self.request(url=url, method=HTTPMetod.POST, json=json or {})

    def put(self, url: str, json: dict | None = None) -> dict:
        return self.request(url=url, method=HTTPMetod.PUT, json=json or {})

    def request(self, url: str, method: HTTPMetod, json: dict | None = None) -> dict:
        def do_request(url: str) -> requests.Response:
            response = requests.request(
                method=method.value,
                url=url,
                headers={"Authorization": f"{self.token.token_type} {self.token.access_token}"},
                json=json,
                timeout=10,
            )
            logger.info(
                "%s %s: %d%s, %d bytes",
                method.name,
                url,
                response.status_code,
                f" {response.reason}" if response.reason else "",
                len(response.content),
            )
            if json:
                logger.debug("json=%s", json)
            return response

        response = do_request(url=url)
        ZohoHTTPError.raise_for_status(response)

        if response.status_code == 204:
            return {}
        return response.json()
