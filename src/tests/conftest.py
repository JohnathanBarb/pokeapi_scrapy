import pytest, httpx, asyncio
import pytest_asyncio

from src.app import app
from asgi_lifespan import LifespanManager
from src.models.pokemon import PokemonDB, Stat
from src.databases.database import get_poke_database, motor_client
from src.tests.config.database import get_test_poke_database


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    app.dependency_overrides[get_poke_database] = get_test_poke_database
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            app=app, base_url="http://app.io"
        ) as test_client:
            yield test_client


@pytest_asyncio.fixture(autouse=True, scope="session")
async def initial_pokemons():
    
    initial_pokemons = [
        PokemonDB(
            name="John1",
            height=185,
            weight=100,
            types=['human'],
            stats=[
                Stat(name='attack', base_stat=10),
                Stat(name='defense', base_stat=10)
            ],
            moves=['move', 'code']
        ),
        PokemonDB(
            name="John2",
            height=185,
            weight=100,
            types=['human'],
            stats=[
                Stat(name='attack', base_stat=10),
                Stat(name='defense', base_stat=10)
            ],
            moves=['move', 'code']
        ),
        PokemonDB(
            name="John3",
            height=185,
            weight=100,
            types=['human'],
            stats=[
                Stat(name='attack', base_stat=10),
                Stat(name='defense', base_stat=10)
            ],
            moves=['move', 'code']),
    ]
    
    await get_test_poke_database().insert_many(
        [pokemon.dict(by_alias=True) for pokemon in initial_pokemons]
    )
    

    yield initial_pokemons
    
    await motor_client.drop_database('pokeapi_test')


