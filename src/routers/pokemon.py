from typing import List

from fastapi import APIRouter, Depends, status

from motor.motor_asyncio import AsyncIOMotorClient

from src.dependencies.get_pokemon import (
    get_pokemon_or_404, get_pokemons_or_404, get_pokemons)
from src.dependencies.api_token import api_token
from src.models.pokemon import (
    PokemonDB, PokemonCreate, PokemonBasicDB, PokemonPartialUpdate)

from src.databases.database import get_poke_database


router = APIRouter()


@router.get('/', summary="Get a List of Pokemons")
async def list_pokemon(
    pokemons: List[PokemonBasicDB] = Depends(get_pokemons)
) -> List[PokemonBasicDB]:
    return pokemons

@router.get('/{id}', summary="Get a Pokemon detail")
async def get_pokemon(
    pokemon: PokemonDB = Depends(get_pokemon_or_404),
) -> PokemonDB:
    return pokemon

@router.post('/', summary="Create a Pokemon")
async def create_pokemon(
    pokemon: PokemonCreate,
    database: AsyncIOMotorClient = Depends(get_poke_database),
) -> PokemonDB:
    """
    Create a Pokemon with all the required information
    """

    pokemon_db = PokemonDB(**pokemon.dict())

    await database.insert_one(pokemon_db.dict(by_alias=True))

    pokemon_db = await get_pokemon_or_404(pokemon_db.id, database)

    return pokemon_db


@router.post('/many', summary="Create multiples Pokemons")
async def create_pokemons(
    pokemons: List[PokemonCreate],
    database: AsyncIOMotorClient = Depends(get_poke_database),
) -> List[PokemonDB]:
    """
    Create Pokemons with all the required information in a list.
    To create a bunch of Pokemons with one request
    """

    pokemons_db = [PokemonDB(**pokemon.dict()) for pokemon in pokemons]
    
    await database.insert_many(
        [pokemon.dict(by_alias=True) for pokemon in pokemons_db]
    )

    pokemons_db = await get_pokemons_or_404(
        [pokemon.dict(
            by_alias=True)['_id'] for pokemon in pokemons_db],
        database,
    )
    
    return pokemons_db


@router.delete('/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Pokemon")
async def delete_pokemon(
    pokemon: PokemonDB = Depends(get_pokemon_or_404),
    database: AsyncIOMotorClient = Depends(get_poke_database)
):
    await database.delete_one({'_id': pokemon.id})


@router.delete('/', 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(api_token)],
    summary="Delete all Pokemons")
async def delete_pokemons(
    database: AsyncIOMotorClient = Depends(get_poke_database)
):
    await database.delete_many({})


@router.patch('/{id}', 
    response_model=PokemonDB,
    summary="Update a Pokemon")
async def update_pokemon(
    pokemon_update: PokemonPartialUpdate,
    pokemon: PokemonDB = Depends(get_pokemon_or_404),
    database: AsyncIOMotorClient = Depends(get_poke_database),
) -> PokemonDB:
    await database.update_one(
        {'_id': pokemon.id},
        {'$set': pokemon_update.dict(exclude_unset=True)}
    )

    pokemon_db = await get_pokemon_or_404(pokemon.id, database)

    return pokemon_db
