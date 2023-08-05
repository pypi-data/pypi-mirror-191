# pylint: skip-file
import asyncio
from typing import AsyncGenerator

import aorta.transport
import pytest
import pytest_asyncio
import ckms.core
from ckms.core import Keychain
from ckms.jose import PayloadCodec
from ckms.types import IKeySpecification
from httpx import AsyncClient

from cbra import Application
from cbra.ext import ioc
from cbra.ext.oauth2 import AccessTokenSigner


@pytest.fixture(scope='session') # type: ignore
def base_url() -> str:
    return "https://cbra.localhost"


@pytest_asyncio.fixture # type: ignore
async def client(
    app: Application,
    base_url: str
) -> AsyncGenerator[AsyncClient, None]:
    await app.on_startup()
    params = {
        'app': app,
        'base_url': base_url
    }
    async with AsyncClient(**params) as client:
        yield client


@pytest.fixture # type: ignore
def codec(app: Application) -> PayloadCodec:
    return app.codec


@pytest.fixture(scope="session") # type: ignore
def event_loop():
    return asyncio.new_event_loop()


@pytest_asyncio.fixture(scope='session') # type: ignore
async def jose_client_signer() -> IKeySpecification:
    return await ckms.core.parse_spec({
        'provider': 'local',
        'kty': 'oct',
        'algorithm': 'HS256',
        'key': {'length': 32}
    })


@pytest.fixture(autouse=True, scope='session') # type: ignore
def inject_message_publisher():
    ioc.provide('MessageTransport', aorta.transport.NullTransport())


@pytest_asyncio.fixture(scope='session') # type: ignore
async def server_keychain() -> Keychain:
    k = Keychain()
    k.configure(
        keys={
            'sig': {
                'provider': 'local',
                'kty': 'OKP',
                'alg': 'EdDSA',
                'crv': 'Ed448',
                'key': {'path': 'pki/sig.key'},
                'use': 'sig'
            },
        }
    )
    await k
    return k

@pytest.fixture # type: ignore
def signing_key() -> str:
    return 'sig'


@pytest.fixture # type: ignore
def token_signer(
    base_url: str,
    server_keychain: Keychain
) -> AccessTokenSigner:
    return AccessTokenSigner(
        issuer=base_url,
        codec=PayloadCodec(
            signer=server_keychain,
            encrypter=server_keychain
        )
    )


@pytest_asyncio.fixture(scope='session') # type: ignore
async def unknown_keychain() -> Keychain:
    k = Keychain()
    k.configure(
        keys={
            'sig': {
                'provider': 'local',
                'kty': 'RSA',
                'key': {'path': 'pki/ext-sig.key'},
                'use': 'sig'
            },
        }
    )
    await k
    return k


@pytest.fixture # type: ignore
def unknown_token_signer(
    base_url: str,
    unknown_keychain: Keychain
) -> AccessTokenSigner:
    return AccessTokenSigner(
        issuer=base_url,
        codec=PayloadCodec(
            signer=unknown_keychain,
            encrypter=unknown_keychain
        )
    )