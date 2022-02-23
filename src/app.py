from fastapi import FastAPI

from src.routers import pokemon

app = FastAPI()
app.include_router(pokemon.router, prefix='/pokemon')

@app.get('/')
async def root():
    return {'message': 'message'}

