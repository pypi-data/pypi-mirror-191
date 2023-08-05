# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.ext.oauth2.types import IPrincipal


class NullPrincipal(IPrincipal): # type: ignore

    def is_authenticated(self) -> bool:
        return False

    def has_scope(self, scope: str | set[str]) -> bool:
        return False