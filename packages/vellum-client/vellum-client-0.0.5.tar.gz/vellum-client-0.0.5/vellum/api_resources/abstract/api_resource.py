from abc import ABC, abstractmethod
from typing import Any, Optional

import requests
from requests import Response

import vellum

from .exceptions import ApiResourceError


class APIResource(ABC):
    @property
    @abstractmethod
    def api_base(self) -> str:
        pass

    @classmethod
    def _construct_url(cls, path: str) -> str:
        return f"{cls.api_base}/{path}"

    @classmethod
    def _construct_headers(cls, headers: Optional[dict] = None) -> dict:
        api_key = vellum.api_key
        return {"X-API-KEY": api_key, **(headers or {})}

    @classmethod
    def _make_request(cls, method: str, path: str, headers: Optional[dict] = None, **kwargs: Any) -> Response:
        url = cls._construct_url(path)
        headers = cls._construct_headers(headers)

        response = requests.request(method, url, headers=headers, **kwargs)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ApiResourceError.from_http_error(e)

        return response
