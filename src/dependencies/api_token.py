import os

from fastapi import Depends, status, HTTPException
from fastapi.security import APIKeyHeader

API_TOKEN = os.getenv('API_TOKEN')

async def api_token(
    token: str = Depends(APIKeyHeader(name='Token'))
):
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN)
