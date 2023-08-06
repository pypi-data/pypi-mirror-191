# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect

import pydantic
from ckms.core import KeySpecification
from ckms.types import CipherText
from ckms.utils import b64encode_str
from ckms.utils import b64decode


class EncryptedValue(pydantic.BaseModel):
    content: str
    iv: str | None = None
    aad: str | None = None
    tag: str | None = None
    encoding: str | None = None

    @property
    def ct(self) -> CipherText:
        return CipherText(
            buf=b64decode(self.content),
            iv=b64decode(self.iv or '') or None,
            aad=b64decode(self.aad or '') or None,
            tag=b64decode(self.tag or '') or None
        )

    @pydantic.validator('aad', pre=True)
    def preprocess_aad(cls, value: bytes | str | None) -> str | None:
        return cls.preprocess_bytes(value=value)

    @pydantic.validator('content', pre=True)
    def preprocess_content(cls, value: bytes | str | None) -> str | None:
        return cls.preprocess_bytes(value=value)

    @pydantic.validator('iv', pre=True)
    def preprocess_iv(cls, value: bytes | str | None) -> str | None:
        return cls.preprocess_bytes(value=value)

    @pydantic.validator('tag', pre=True)
    def preprocess_tag(cls, value: bytes | str | None) -> str | None:
        return cls.preprocess_bytes(value=value)

    @classmethod
    def preprocess_bytes(cls, value: bytes | str | None) -> str | None:
        if isinstance(value, bytes):
            value = b64encode_str(value)
        return value

    async def decrypt(self, key: KeySpecification) -> bytes | str:
        pt = key.decrypt(self.ct)
        if inspect.isawaitable(pt):
            pt = await pt
        assert isinstance(pt, bytes) # nosec
        if self.encoding:
            pt = bytes.decode(pt, self.encoding)
        return pt