from typing import Any, Dict, Optional

import httpx
from pydantic import BaseModel

from .exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQlClientInvalidResponseError,
)


class BaseClient:
    def __init__(
        self,
        base_url: str = "",
        headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self.base_url = base_url
        self.headers = headers

        self.http_client = (
            http_client
            if http_client
            else httpx.Client(base_url=base_url, headers=headers)
        )

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:
        self.http_client.close()

    def execute(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        payload: Dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = self._convert_dict_to_json_serializable(variables)
        return self.http_client.post(url="/graphql/", json=payload)

    def get_data(self, response: httpx.Response) -> dict:
        if not response.is_success:
            raise GraphQLClientHttpError(
                status_code=response.status_code, response=response
            )

        try:
            response_json = response.json()
        except ValueError as exc:
            raise GraphQlClientInvalidResponseError(response=response) from exc

        if (not isinstance(response_json, dict)) or ("data" not in response_json):
            raise GraphQlClientInvalidResponseError(response=response)

        data = response_json["data"]
        errors = response_json.get("errors")

        if errors:
            raise GraphQLClientGraphQLMultiError.from_errors_dicts(
                errors_dicts=errors, data=data
            )

        return data

    def _convert_dict_to_json_serializable(self, dict_: Dict[str, Any]):
        return {
            key: value
            if not isinstance(value, BaseModel)
            else value.dict(by_alias=True)
            for key, value in dict_.items()
        }
