from fastapi import APIRouter

from src.dependencies.object_id import get_object_id
from src.dependencies.get_pokemon import get_pokemon_or_404
from src.dependencies.pagination import pagination

from src.databases.database import (
    get_database, database
)

router = APIRouter()

