from __future__ import annotations

import json

from requests import HTTPError


class ApiResourceError(HTTPError):
    def __str__(self) -> str:
        return f"ApiResourceError({self.args[0]}. Details: {self.details})"

    @property
    def details(self) -> str:
        try:
            return json.dumps(self.response.json())
        except json.JSONDecodeError:
            return "N/A"

    @classmethod
    def from_http_error(cls, http_error: HTTPError) -> ApiResourceError:
        return cls(http_error.args[0], response=http_error.response)
