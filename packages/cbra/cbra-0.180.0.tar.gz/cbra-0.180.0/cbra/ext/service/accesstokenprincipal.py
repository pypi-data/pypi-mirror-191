# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re

import pydantic
from ckms.types import JSONWebToken
from ckms.types import MalformedPayload

from cbra.ext.oauth2.types import IPrincipal
from .clientprincipal import ClientPrincipal
from .subjectprincipal import SubjectPrincipal


class AccessTokenPrincipal(pydantic.BaseModel, IPrincipal):
    __root__: ClientPrincipal | SubjectPrincipal

    def has_scope(
        self,
        scope: str | set[str]
    ) -> bool:
        """Return a boolean indicating if the :class:`AccessTokenPrincipal` is
        authorized to use the given `scope`.
        """
        if isinstance(scope, str):
            scope = {scope}
        return scope <= self.__root__.scope

    @classmethod
    def fromclaimset(cls, claims: JSONWebToken) -> 'AccessTokenPrincipal':
        assert claims.sub is not None # nosec
        scope = []
        if 'scope' in claims.extra:
            if not isinstance(claims.extra['scope'], str):
                raise MalformedPayload(
                    message="The 'scope' parameter must be a space-separated string."
                )
            scope = re.split('\\s', claims.extra['scope'])
        return cls.parse_obj({
            **claims.dict(),
            'scope': scope
        })

    def is_authenticated(self) -> bool:
        return self.__root__.is_authenticated()