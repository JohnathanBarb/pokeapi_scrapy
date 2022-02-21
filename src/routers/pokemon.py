from fastapi import APIRouter

from src.dependencies.pagination import pagination
from src.databases.database import (
    get_database, database
)

router = APIRouter()

