from pydantic import BaseModel
from fastapi import APIRouter
from .methods import get_location


router = APIRouter()

class City(BaseModel):
    city: str


@router.post("/")
def search_city(data: City) -> dict:
    return get_location(data.dict())



