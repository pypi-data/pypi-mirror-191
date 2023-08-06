# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import httpx
from ckms.utils import current_timestamp

from .icredential import ICredential


class AccessTokenCredential(ICredential):
    """An OAuth 2.0 access token."""
    __module__: str = 'cbra.ext.api.credential'
    expires: int
    token: str
    refresh_token: str | None

    def __init__(self, token: str, expires_in: int, refresh_token: str | None = None):
        self.token = token
        self.expires = current_timestamp() + expires_in
        self.refresh_token = refresh_token

    async def add_to_request(self, request: httpx.Request) -> None:
        request.headers['Authorization'] = f'Bearer {self.token}'