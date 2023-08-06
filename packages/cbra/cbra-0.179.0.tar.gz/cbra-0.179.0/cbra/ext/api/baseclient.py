# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any
from typing import Callable
from typing import NoReturn
from typing import TypeVar

import httpx

from cbra.exceptions import NotFound
from .credential import ICredential


M = TypeVar('M')


class BaseClient(httpx.AsyncClient):
    __module__: str = 'cbra.ext.api'
    credential: ICredential
    logger: logging.Logger = logging.getLogger('uvicorn')

    def __init__(
        self,
        *,
        credential: ICredential,
        **kwargs: Any
    ):
        self.credential = credential
        super().__init__(**{
            **kwargs,
            **self.get_http_client_kwargs()
        })

    def get_http_client_kwargs(self) -> dict[str, Any]:
        raise NotImplementedError

    async def request_resource(
        self,
        method: str,
        response_model: Callable[..., M],
        credential: ICredential | None = None,
        *args: Any,
        **kwargs: Any
    ) -> M:
        credential = credential or self.credential
        request = await self.request_factory(
            method=method,
            credential=credential,
            *args,
            **kwargs
        )
        response = await credential.send(self, request)
        if response.status_code == 404:
            raise NotFound
        await self.process_response(request, response)
        response.raise_for_status()
        return response_model(response.json())

    async def request_factory(
        self,
        method: str,
        json: Any | None = None,
        credential: ICredential | None = None,
        *args: Any,
        **kwargs: Any
    ) -> httpx.Request:
        """Create a :class:`httpx.Request` instance."""
        credential = credential or self.credential
        if json is not None:
            kwargs['json'] = await self.preprocess_json(json, credential=credential)
        request = self.build_request(method=method, *args, **kwargs) # type: ignore
        await credential.add_to_request(request)
        return request

    async def preprocess_json(
        self,
        json: dict[str, Any] | list[Any],
        credential: ICredential
    ) -> dict[str, Any] | list[Any]:
        """Preprocess the JSON payload of a request."""
        return await credential.preprocess_json(json)

    async def process_response(
        self,
        request: httpx.Request,
        response: httpx.Response
    ) -> httpx.Response:
        if response.status_code >= 400:
            await self.on_error(request, response)
        return response

    async def on_error(
        self,
        request: httpx.Request,
        response: httpx.Response
    ) -> NoReturn | None:
        self.logger.warning(
            "Service returned a non-2xx response (%s)",
            response.status_code
        )
        if 400 <= response.status_code < 500:
            await self.on_client_error(request, response)
        if 500 <= response.status_code:
            await self.on_server_error(request, response)

    async def on_client_error(
        self,
        request: httpx.Request,
        response: httpx.Response
    ) -> NoReturn:
        raise httpx.HTTPStatusError(
            message='Client error',
            request=request,
            response=response
        )

    async def on_server_error(
        self,
        request: httpx.Request,
        response: httpx.Response
    ) -> NoReturn:
        httpx.HTTPStatusError
        raise httpx.HTTPStatusError(
            message='Server error',
            request=request,
            response=response
        )