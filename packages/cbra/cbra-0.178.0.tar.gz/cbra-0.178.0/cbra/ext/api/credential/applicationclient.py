# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os

import httpx
from ckms.core import parse_dsn
from ckms.core import parse_spec
from ckms.core import KeySpecification
from ckms.types import ServerMetadata

from .accesstoken import AccessTokenCredential
from .icredential import ICredential
from .jwtprivatekeyclientcredential import JWTPrivateKeyClientCredential


class ApplicationClientCredential(ICredential):
    """A credential implementation that uses an application-specific
    signing/encryption keypair to retrieve an access token from an
    OAuth 2.x authorization server.
    """
    access_tokens: dict[tuple[str, str], AccessTokenCredential] = {}
    server: str | None = os.getenv('OAUTH_SERVER')
    client_id: str | None = os.getenv('OAUTH_SERVICE_CLIENT')
    client_credential: JWTPrivateKeyClientCredential
    metadata: ServerMetadata | None = None
    encryption_key: KeySpecification | None = None
    signing_key: KeySpecification | None = None

    def __init__(self):
        if os.getenv('APP_ENCRYPTION_KEY'):
            self.encryption_key = parse_spec(parse_dsn(os.environ['APP_ENCRYPTION_KEY']))
        if os.getenv('APP_SIGNING_KEY'):
            self.signing_key = parse_spec(parse_dsn(os.environ['APP_SIGNING_KEY']))
        self.access_tokens = type(self).access_tokens

    async def add_to_request(self, request: httpx.Request) -> None:
        """Add the access token to a request as the ``Authorization``
        header.

        If no access token is maintained for the given audience, then invoke the
        token endpoint of the authorization server to obtain one.
        """
        assert self.client_id is not None # nosec
        _, audience = k = (
            self.client_id,
            f'{request.url.scheme}://{request.url.netloc.decode()}'
        )
        at = self.access_tokens.get(k)
        if at is None:
            at = self.access_tokens[k] = await self.obtain(audience=audience)
        return await at.add_to_request(request)

    async def obtain(self, audience: str) -> AccessTokenCredential:
        """Obtain an access token from the authorization server using the Client
        Credentials grant.
        """
        assert self.client_id is not None # nosec
        assert self.server is not None # nosec
        assert self.signing_key is not None # nosec
        await self.signing_key
        if self.encryption_key is not None:
            await self.encryption_key
        async with httpx.AsyncClient() as client:
            if self.metadata is None:
                self.metadata = await ServerMetadata.discover(
                    client=client,
                    issuer=self.server
                )
            assert self.metadata is not None # nosec
            endpoint = self.metadata.token_endpoint
        credential = JWTPrivateKeyClientCredential(
            client_id=self.client_id,
            token_endpoint=endpoint,
            signing_key=self.signing_key,
            encryption_key=None
        )
        return await credential.obtain(audience=audience)