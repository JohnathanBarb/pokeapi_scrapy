import os
from motor.motor_asyncio import AsyncIOMotorClient
from src.databases.database import motor_client

username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

database_test = motor_client['pokeapi_test']

def get_test_poke_database():
    return database_test['pokemons']
