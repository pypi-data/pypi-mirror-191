# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets

import httpx
from ckms.core import KeySpecification
from ckms.jose import PayloadCodec
from ckms.utils import current_timestamp

from cbra.ext.oauth2.types import TokenResponse
from .accesstoken import AccessTokenCredential
from .clientcredential import ClientCredential


class JWTPrivateKeyClientCredential(ClientCredential):
    """The ``private_key_jwt`` authentication method used by the token
    endpoint.
    """
    __module__: str = 'cbra.ext.api.credential'
    access_token: AccessTokenCredential | None
    client_assertion_type: str = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    codec: PayloadCodec
    encryption_key: KeySpecification | None
    signing_key: KeySpecification
    token_endpoint: str

    def __init__(
        self,
        client_id: str,
        token_endpoint: str,
        signing_key: KeySpecification,
        encryption_key: KeySpecification | None
    ):
        super().__init__(client_id=client_id)
        self.access_token = None
        self.client_id = client_id
        self.encryption_key = encryption_key
        self.signing_key = signing_key
        self.token_endpoint = token_endpoint
        self.codec = PayloadCodec(
            signing_keys=[self.signing_key],
        )

    async def obtain(self, audience: str) -> AccessTokenCredential:
        """Obtain an access token using the client credentials grant."""
        params: dict[str, str] = {
            'client_id': self.client_id,
            'client_assertion_type': self.client_assertion_type,
            'client_assertion': await self.create_assertion(sub=self.client_id),
            'grant_type': 'client_credentials',
            'resource': audience
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url=self.token_endpoint, json=params) # type: ignore
            if response.status_code != 200:
                raise Exception(response.content)
            result = TokenResponse.parse_obj(response.json())
        return AccessTokenCredential(
            token=result.access_token,
            expires_in=result.expires_in,
            refresh_token=result.refresh_token
        )

    async def create_assertion(self, **claims: int | str) -> str:
        """Create the assertion used to authenticate with the token endpoint."""
        return await self.codec.encode(
            payload=self.get_claims(**claims)
        )

    def get_claims(self, **extra: int | str) -> dict[str, int | str]:
        """Return a dictionary containing the JWT claims used to
        construct the client assertion or JAR.
        """
        now = current_timestamp()
        return {
            **extra,
            'aud': self.token_endpoint,
            'client_id': self.client_id,
            'exp': now + 60,
            'iat': now,
            'iss': self.client_id,
            'jti': secrets.token_urlsafe(48),
            'nbf': now
        }