import os
from motor.motor_asyncio import (
    AsyncIOMotorClient
)

username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

motor_client = AsyncIOMotorClient(
    f'mongodb://{username}:{password}@mongodb:27017/?authSource=admin')
database = motor_client['pokeapi']

def get_database() -> AsyncIOMotorClient:
    return database

def get_poke_database() -> AsyncIOMotorClient:
    return database['pokemons']
