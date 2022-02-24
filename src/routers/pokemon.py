from typing import List

from fastapi import APIRouter, Depends, status

from motor.motor_asyncio import AsyncIOMotorClient

from src.dependencies.object_id import get_object_id
from src.dependencies.get_pokemon import (
    get_pokemon_or_404, get_pokemons_or_404)
from src.dependencies.pagination import pagination

from src.models.pokemon import (
    PokemonDB, PokemonCreate, PokemonBasicDB)

from src.databases.database import (
    get_database, database)


router = APIRouter()


@router.get('/')
async def list_pokemon(
    pagination: pagination = Depends(pagination),
    database: AsyncIOMotorClient = Depends(get_database),
) -> List[PokemonBasicDB]:
    skip, limit = pagination
    query = database['pokemons'].find(
        {}, skip=skip, limit=limit)
    
    pokemons = [
        PokemonBasicDB(**raw_pokemon) async for raw_pokemon in query
    ]

    return pokemons

@router.get('/{id}')
async def get_pokemon(
    pokemon: PokemonDB = Depends(get_pokemon_or_404),
) -> PokemonDB:
    return pokemon

@router.post('/')
async def create_pokemon(
    pokemon: PokemonCreate,
    database: AsyncIOMotorClient = Depends(get_database),
) -> PokemonDB:
    pokemon_db = PokemonDB(**pokemon.dict())

    await database['pokemons'].insert_one(pokemon_db.dict(by_alias=True))

    pokemon_db = await get_pokemon_or_404(pokemon_db.id, database)

    return pokemon_db


@router.post('/many')
async def create_pokemons(
    pokemons: List[PokemonCreate],
    database: AsyncIOMotorClient = Depends(get_database),
) -> List[PokemonDB]:
    pokemons_db = [PokemonDB(**pokemon.dict()) for pokemon in pokemons]
    
    await database['pokemons'].insert_many(
        [pokemon.dict(by_alias=True) for pokemon in pokemons_db]
    )

    pokemons_db = await get_pokemons_or_404(
        [pokemon.dict(
            by_alias=True)['_id'] for pokemon in pokemons_db],
        database,
    )
    
    return pokemons_db


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pokemon(
    pokemon: PokemonDB = Depends(get_pokemon_or_404),
    database: AsyncIOMotorClient = Depends(get_database)
):
    await database['pokemons'].delete_one({'_id': pokemon.id})


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pokemons(
    database: AsyncIOMotorClient = Depends(get_database)
):
    await database['pokemons'].delete_many({})
