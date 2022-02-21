from fastapi import FastAPI

from src.routers import pokemon

app = FastAPI()

app.include_router(pokemon.router)


