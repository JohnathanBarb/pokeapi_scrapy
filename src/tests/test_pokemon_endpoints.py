from typing import List
import pytest, httpx

from fastapi import status
from src.models.pokemon import PokemonDB

from src.tests.conftest import test_client, initial_pokemons

@pytest.mark.asyncio
async def test_home(
        test_client: httpx.AsyncClient
    ):
    response = await test_client.get('/')

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json == {
        'message':
            'Welcome to PokeAPI Scrapy madded by Johnathan Barbosa'
    }


@pytest.mark.asyncio
class TestGetPokemon:
    async def test_not_existing(
        self,
        test_client: httpx.AsyncClient
    ):
        response = await test_client.get(
            f'/pokemons/321412')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

        json = response.json()

        assert json['detail'] == "Not Found"
        
        

    async def test_existing(
        self,
        test_client: httpx.AsyncClient,
        initial_pokemons: List[PokemonDB]
    ):
        response = await test_client.get(
            f'/pokemons/{initial_pokemons[0].id}')
        
        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json["_id"] == str(initial_pokemons[0].id)
