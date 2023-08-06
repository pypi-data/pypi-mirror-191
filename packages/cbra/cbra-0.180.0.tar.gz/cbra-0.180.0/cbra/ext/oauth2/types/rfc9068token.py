"""Declares :class:`RFC9068Token`."""
from typing import Any

from ckms.jose import PayloadCodec
from ckms.types import AudienceType
from ckms.types import ClaimSet

from .spaceseparatedlist import SpaceSeparatedList


class RFC9068Token(ClaimSet):
    iss: str
    aud: AudienceType
    exp: int
    sub: int | str
    client_id: str
    iat: int
    jti: str
    auth_time: int | None = None
    acr: str | None = None
    amr: list[str] | None = []
    scope: SpaceSeparatedList = SpaceSeparatedList()

    async def sign(self, codec: PayloadCodec, **kwargs: Any) -> str:
        """Sign the token using the given encoder."""
        return await codec.encode(
            payload={
                **self.dict(),
                'aud': list(self.aud)[0] if len(self.aud) == 1 else list(sorted(self.aud)),
                'scope': str(self.scope)
            },
            **kwargs
        )

    class Config(ClaimSet.Config):
        json_encoders = {
            **ClaimSet.Config.json_encoders,
            SpaceSeparatedList: lambda v: str.join(' ', sorted(v)) # type: ignore
        }