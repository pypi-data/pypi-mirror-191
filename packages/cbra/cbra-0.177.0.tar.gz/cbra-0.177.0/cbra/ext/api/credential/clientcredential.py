# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .icredential import ICredential


class ClientCredential(ICredential):
    """The base class for OAuth 2.0 client credentials. A client credential
    obtains an access token credential from the authorization server.
    """
    __module__: str = 'cbra.ext.api.credential'
    client_id: str
    client_assertion_type: str

    def __init__(
        self,
        client_id: str
    ):
        self.client_id = client_id