# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets
from typing import Any

from ckms.jose import PayloadCodec
from ckms.utils import current_timestamp


class AccessTokenSigner:
    __module__: str = 'cbra.ext.oauth2'
    client_id: Any
    codec: PayloadCodec
    default_ttl: int
    issuer: str
    entropy: int
    signing_keys: list[str]

    def __init__(
        self,
        *,
        issuer: str,
        codec: PayloadCodec,
        client_id: Any = None,
        entropy: int = 48,
        default_ttl: int = 600,
        signing_keys: list[str] | None = None
    ):
        self.client_id = client_id
        self.codec = codec
        self.default_ttl = default_ttl
        self.entropy = entropy
        self.issuer = issuer
        self.signing_keys = signing_keys or []

    def initialize_claims(
        self,
        now: int | None = None,
        ttl: int | None = None,
        **claims: Any
    ) -> dict[str, int | str]:
        """Initialize the default claims ``exp``, ``iat``, ``jti``, ``nbf``
        and ``iss``.
        """
        now = now or current_timestamp()
        return {
            'exp': now + (ttl or self.default_ttl),
            'iat': now,
            'iss': self.issuer,
            'jti': secrets.token_urlsafe(48),
            'nbf': now
        }

    async def sign(
        self,
        *,
        audience: str,
        sub: int | str,
        client_id: Any = None,
        ttl: int | None = None,
        now: int | None = None,
        signing_keys: list[str] | None = None,
        scope: str | set[str] | list[str] | None = None,
        content_type: str = 'at+jwt',
        **claims: Any
    ) -> str:
        """Sign a :rfc:`9068` access token with the given claims."""
        if not isinstance(scope, str):
            scope = str.join(' ', list(sorted(scope or [])))
        if not (signing_keys or self.signing_keys):
            raise TypeError("The `signing_keys` parameter can not be `None`.")
        if not (client_id or self.client_id):
            raise TypeError("The `client_id` parameter can not be `None`.")
        return await self.codec.encode(
            payload={
                **self.initialize_claims(now=now, ttl=ttl),
                **claims,
                'aud': audience,
                'client_id': client_id or self.client_id,
                'sub': sub,
                'scope': scope
            },
            content_type=content_type,
            signing_keys=signing_keys or self.signing_keys
        )