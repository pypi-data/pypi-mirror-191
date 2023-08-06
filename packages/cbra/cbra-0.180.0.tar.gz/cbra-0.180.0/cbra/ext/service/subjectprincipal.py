# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

from cbra.ext.oauth2.types import IPrincipal
from cbra.ext.oauth2.types import RFC9068Token


class SubjectPrincipal(IPrincipal, RFC9068Token): # type: ignore
    sub: int

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        if values.get('sub') == values.get('client_id'):
            raise ValueError(
                "The token does not authenticate a Subject."
            )
        return values

    def is_authenticated(self) -> bool:
        return True