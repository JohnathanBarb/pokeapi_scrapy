from typing import List
from bson import ObjectId, errors
from fastapi import HTTPException, status

async def get_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except (errors.InvalidId, TypeError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

async def get_objects_id(ids: List[str]) -> List[ObjectId]:
    try:
        return [ObjectId(id) for id in ids]
    except (errors.InvalidId, TypeError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
