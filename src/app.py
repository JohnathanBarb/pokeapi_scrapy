from fastapi import FastAPI

from routers import pokemon

app = FastAPI()

app.include_router(pokemon.router)


