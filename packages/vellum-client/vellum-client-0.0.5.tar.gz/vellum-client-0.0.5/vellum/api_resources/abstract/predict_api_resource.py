from abc import abstractmethod
from typing import Any, cast

from vellum.api_resources.abstract.api_resource import APIResource


class PredictAPIResource(APIResource):
    @property
    @abstractmethod
    def api_path(self) -> str:
        pass

    api_base = "https://predict.vellum.ai"

    @classmethod
    def run(cls, **kwargs: Any) -> dict:
        result = cast(dict, cls._make_request("POST", cast(str, cls.api_path), json=kwargs).json())

        return result
