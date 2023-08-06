"""Declares :class:`AuthorizationEndpointTest`."""
import pytest
from httpx import AsyncClient

from cbra.ext.oauth2 import AccessTokenSigner


@pytest.mark.asyncio
async def test_authentication_is_required(
    client: AsyncClient,
    path: str,
):
    response = await client.get(
        url=path,
    )
    assert response.status_code == 401, response.content


@pytest.mark.asyncio
async def test_authenticate_subject(
    base_url: str,
    client: AsyncClient,
    path: str,
    signer: AccessTokenSigner,
    signing_key: str
):
    at = await signer.sign(
        client_id='test',
        audience=base_url,
        sub=1,
        signing_keys=[signing_key]
    )
    response = await client.get(
        url=path,
        headers={'Authorization': f'Bearer {at}'}
    )
    assert response.status_code == 200, response.content


@pytest.mark.asyncio
async def test_invalid_token_type_is_rejected(
    base_url: str,
    client: AsyncClient,
    path: str,
    signer: AccessTokenSigner,
    signing_key: str
):
    at = await signer.sign(
        client_id='test',
        audience=base_url,
        sub=1,
        content_type="jwt",
        signing_keys=[signing_key]
    )
    response = await client.get(
        url=path,
        headers={'Authorization': f'Bearer {at}'}
    )
    assert response.status_code == 400, response.status_code


@pytest.mark.asyncio
async def test_expired_token_is_rejected(
    base_url: str,
    client: AsyncClient,
    path: str,
    signer: AccessTokenSigner,
    signing_key: str
):
    at = await signer.sign(
        client_id='test',
        audience=base_url,
        sub=1,
        signing_keys=[signing_key],
        now=1
    )
    response = await client.get(
        url=path,
        headers={'Authorization': f'Bearer {at}'}
    )
    assert response.status_code == 403, response.status_code


@pytest.mark.asyncio
async def test_invalid_audience_is_rejected(
    client: AsyncClient,
    path: str,
    signer: AccessTokenSigner,
    signing_key: str
):
    at = await signer.sign(
        client_id='test',
        audience="https://www.example.com",
        sub=1,
        signing_keys=[signing_key],
        now=1
    )
    response = await client.get(
        url=path,
        headers={'Authorization': f'Bearer {at}'}
    )
    assert response.status_code == 403, response.status_code


@pytest.mark.asyncio
async def test_unkown_signer_is_rejected_for_local_audience(
    base_url: str,
    client: AsyncClient,
    path: str,
    unknown_signer: AccessTokenSigner,
    signing_key: str
):
    at = await unknown_signer.sign(
        client_id='test',
        audience=base_url,
        sub=1,
        signing_keys=[signing_key],
    )
    response = await client.get(
        url=path,
        headers={'Authorization': f'Bearer {at}'}
    )
    assert response.status_code == 403, response.status_code