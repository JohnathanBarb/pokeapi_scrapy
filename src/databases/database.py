from motor.motor_asyncio import (
    AsyncIOMotorClient
)

motor_client = AsyncIOMotorClient('mongodb://mongoadmin:secret@localhost:27888/?authSource=admin')
database = motor_client['pokeapi']

def get_database() -> AsyncIOMotorClient:
    return database
