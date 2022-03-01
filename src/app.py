from fastapi import FastAPI

from src.routers import pokemon

app = FastAPI()

@app.get('/', tags=['Welcome'])
async def root():
    return {
        'message':
            'Welcome to PokeAPI Scrapy madded by Johnathan Barbosa'
    }


app.include_router(pokemon.router, prefix='/pokemons', tags=['Pokemon'])
