from fastapi import Depends, HTTPException, status
from object_id import get_object_id
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.databases.database import get_database
from src.models.pokemon import PokemonDB

from bson import ObjectId

async def get_pokemon_or_404(
    id: ObjectId = Depends(get_object_id),
    database: AsyncIOMotorDatabase = Depends(get_database)
) -> PokemonDB:
    raw_pokemon = await database['pokemons'].find_one({'_id': id})
    if raw_pokemon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return PokemonDB(**raw_pokemon)
