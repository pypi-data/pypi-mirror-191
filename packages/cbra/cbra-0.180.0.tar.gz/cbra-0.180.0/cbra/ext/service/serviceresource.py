# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
from ckms.core import Keychain
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from cbra.ext.oauth2 import RFC9068Principal
from cbra.ext.oauth2.params import LocalIssuer
from cbra.params import ServerKeychain
from cbra.resource import Resource
from .accesstokenprincipal import AccessTokenPrincipal
from .nullprincipal import NullPrincipal


class ServiceResource(Resource):
    """A :class:`cbra.resource.Resource` implementation that authenticates
    a service with a :rfc:`9068` access token.
    """
    __abstract__: bool = True
    __module__: str = 'cbra.ext.service'
    principal: AccessTokenPrincipal
    security = HTTPBearer(auto_error=False)
    trusted_issuers: set[str] = set()

    @classmethod
    async def principal_factory(
        cls,
        request: fastapi.Request,
        issuer: str = LocalIssuer,
        bearer: HTTPAuthorizationCredentials | None = fastapi.Depends(security),
        keychain: Keychain = ServerKeychain
    ) -> AccessTokenPrincipal | NullPrincipal:
        f = RFC9068Principal(
            auto_error=cls.require_authentication,
            principal_factory=AccessTokenPrincipal.fromclaimset,
            trusted_issuers=cls.trusted_issuers
        )
        return await f(
            request=request,
            issuer=issuer,
            bearer=bearer,
            keychain=keychain
        ) or NullPrincipal()

    def is_authenticated(self) -> bool:
        """Return a boolean indicating if the request is authenticated."""
        return self.principal is not None and self.principal.is_authenticated()