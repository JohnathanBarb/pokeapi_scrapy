from motor.motor_asyncio import (
    AsyncIOMotorClient
)

motor_client = AsyncIOMotorClient('mongodb://localhost:27017')
database = motor_client['pokeapi_pokemon']

def get_database() -> AsyncIOMotorClient:
    return database
