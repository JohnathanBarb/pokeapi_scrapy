from typing import Tuple
from fastapi import Query

async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0)
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)
