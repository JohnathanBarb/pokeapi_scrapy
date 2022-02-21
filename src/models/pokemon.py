from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(
                        default_factory=PyObjectId, alias='_id')
    
    class Config:
        json_encoders = {ObjectId: str}


class Stat(BaseModel):
    name: str
    base_stat: str


class PokemonBase(MongoBaseModel):
    name: str
    height: int
    weight: int
    types: List[str]
    stats: List[Stat]
    moves: List[str]


class PokemonCreate(PokemonBase):
    pass


class PokemonDB(PokemonBase):
    pass


class PokemonPartialUpdate(BaseModel):
    name: Optional[str]
    name: Optional[str]
    height: Optional[int]
    weight: Optional[int]
    types: Optional[List[str]]
    stats: Optional[List[Stat]]
    moves: Optional[List[str]]
