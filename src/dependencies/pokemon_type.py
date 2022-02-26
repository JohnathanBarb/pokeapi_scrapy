from typing import Dict, List, Optional
from fastapi import Query

async def poke_type(
    type: str = Query(None),
) -> Dict:
    if type is None:
        return {}
    return {"types": {"$in": [type]}}
