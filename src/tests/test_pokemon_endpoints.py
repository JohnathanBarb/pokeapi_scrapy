import pytest, httpx

from fastapi import status

from src.tests.utils.conftest import test_client

@pytest.mark.asyncio
async def test_home(test_client: httpx.AsyncClient):
    response = await test_client.get('/')

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json == {
        'message':
            'Welcome to PokeAPI Scrapy madded by Johnathan Barbosa'
    }
