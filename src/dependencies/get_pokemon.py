from typing import List
from fastapi import Depends, HTTPException, status
from src.dependencies.object_id import (
    get_object_id, get_objects_id
)
from src.dependencies.pagination import pagination
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.databases.database import get_poke_database
from src.models.pokemon import PokemonBasicDB, PokemonDB

from bson import ObjectId

async def get_pokemon_or_404(
    id: ObjectId = Depends(get_object_id),
    database: AsyncIOMotorDatabase = Depends(get_poke_database)
) -> PokemonDB:
    raw_pokemon = await database.find_one({'_id': id})
    if raw_pokemon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return PokemonDB(**raw_pokemon)

async def get_pokemons_or_404(
    ids: List[ObjectId] = Depends(get_objects_id),
    database: AsyncIOMotorDatabase = Depends(get_poke_database)
) -> List[PokemonDB]:
    query = database.find(
        {'_id': {'$in': ids}})
    
    pokemons = [PokemonDB(**raw_pokemon) async for raw_pokemon in query]
    if pokemons is None or len(pokemons) != len(ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return pokemons


async def get_pokemons(
    database: AsyncIOMotorDatabase = Depends(get_poke_database),
    pagination: pagination = Depends(pagination)
) -> List[PokemonBasicDB]:
    skip, limit = pagination
    query = database.find(
        {}, skip=skip, limit=limit)

    return [PokemonBasicDB(**raw_pokemon) async for raw_pokemon in query]
