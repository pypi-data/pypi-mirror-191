# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest
from ckms.core import Keychain

from cbra import Application
from cbra.ext.service import ServiceResource
from cbra.ext.oauth2 import AccessTokenSigner
from cbra.ext.oauth2.tests.authorization import *


@pytest.fixture
def app(server_keychain: Keychain) -> Application:
    app = Application(
        keychain=server_keychain
    )
    app.add(ObjectResource)
    return app


@pytest.fixture
def path() -> str:
    return '/objects'


@pytest.fixture
def signer(token_signer: AccessTokenSigner) -> AccessTokenSigner:
    return token_signer


@pytest.fixture
def unknown_signer(unknown_token_signer: AccessTokenSigner) -> AccessTokenSigner:
    return unknown_token_signer


class ObjectResource(ServiceResource):
    path_parameter: str = 'object_id'

    async def list(self):
        pass