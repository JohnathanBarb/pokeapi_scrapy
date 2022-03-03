from typing import List
import pytest, httpx

from fastapi import status
from src.models.pokemon import PokemonDB, Stat

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


@pytest.mark.asyncio
class TestPostPokemon:
    async def test_with_missing_data(
        self,
        test_client: httpx.AsyncClient,
    ):
        response = await test_client.post(
            '/pokemons/',
            data='{"name": "poke_test", "height": 10}'
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        json = response.json()

        assert json['detail'][0]['msg'] == "field required"
    

    async def test_with_correct_data(
        self,
        test_client: httpx.AsyncClient,
    ):
        data = PokemonDB(
            name="John1",
            height=185,
            weight=100,
            types=['human'],
            stats=[
                Stat(name='attack', base_stat=10),
                Stat(name='defense', base_stat=10)
            ],
            moves=['move', 'code']
        )

        response = await test_client.post(
            '/pokemons/',
            content=data.json()
        )

        assert response.status_code == status.HTTP_200_OK

        json = response.json()

        assert json['name'] == data.name


@pytest.mark.asyncio
class TestPutPokemon:
    async def test_patch_with_not_existing_pokemon(
        self,
        test_client: httpx.AsyncClient
    ):
        id = 'not-valid-objectid'
        response = await test_client.patch(
            f'/pokemons/{id}',
            content='{"name": "poke_test", "height": 10}')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    

    async def test_patch_pokemon_correct(
        self,
        test_client: httpx.AsyncClient,
        initial_pokemons: List[PokemonDB]
    ):
        response = await test_client.patch(
            f'/pokemons/{initial_pokemons[0].id}',
            content='{"name": "poke_test", "height": 10}')
        
        assert response.status_code == status.HTTP_200_OK

        json = response.json()

        assert json['name'] == 'poke_test'


@pytest.mark.asyncio
class TestDeletePokemon:
    async def test_delete_a_not_existing_pokemon(
        self,
        test_client: httpx.AsyncClient
    ):
        id = 'not-valid-objectid'
        response = await test_client.delete(
            f'/pokemons/{id}')

        assert response.status_code == status.HTTP_404_NOT_FOUND


    async def test_delete_a_existing_pokemon(
        self,
        test_client: httpx.AsyncClient,
        initial_pokemons: List[PokemonDB],
    ):
        response = await test_client.delete(
            f'/pokemons/{initial_pokemons[0].id}'
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
