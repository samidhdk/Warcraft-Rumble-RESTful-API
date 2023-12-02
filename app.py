from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from Rumble import Rumble
from bson import json_util
from fastapi import FastAPI, Path, Query, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import uvicorn
import pymongo

uri = "mongodb+srv://..."
app = FastAPI()
client = MongoClient(uri, server_api=ServerApi('1'))

rumble = Rumble()
db = client.test
collection = db.rumble_collection


class Card(BaseModel):
    id: int
    cost: int
    name: str
    faction: str
    type: str
    description: str
    traits: list[str]


def json_encoder(obj):
    if isinstance(obj, pymongo.objectid.ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


@app.get("/", include_in_schema=False)
async def redirect():
    response = RedirectResponse(url="/docs")
    return response


@app.get("/units")
async def get_all_units():
    cursor = collection.find({}, {'_id': 0})
    json_results = json_util.dumps(cursor, default=json_encoder)
    return json_results


@app.get("/units/{unit_id}")
async def get_unit_by_id(unit_id: int = Path(..., description="The ID of the unit you would like to retrieve")):
    cursor = collection.find_one({'id': unit_id}, {'_id': 0})
    if cursor:
        json_results = json_util.dumps(cursor, default=json_encoder)
        return json_results
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit id not found")


@app.get("/units/faction/{unit_faction}")
async def get_units_by_faction(
        unit_faction: str = Path(..., description="The faction of the unit you would like to retrieve")):
    unit_faction = unit_faction.lower()
    factions = {"horde", "blackrock", "alliance", "beast", "undead"}
    if unit_faction in factions:
        unit_faction = unit_faction.title()
        cursor = collection.find({'faction': unit_faction}, {'_id': 0})
        if cursor:
            json_results = json_util.dumps(cursor, default=json_encoder)
            return json_results
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit faction not found")


@app.get("/units/type/{unit_type}")
async def get_units_by_type(unit_type: str):
    unit_type = unit_type.lower()
    types = {"troop", "spell", "leader"}
    if unit_type in types:
        unit_type = unit_type.title()
        cursor = collection.find({'type': unit_type}, {'_id': 0})
        if cursor:
            json_results = json_util.dumps(cursor, default=json_encoder)
            return json_results
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit type not found")


@app.get("/units/cost/{unit_cost}")
async def get_units_by_cost(unit_cost: int = Path(..., description="The cost of the units you want to retrieve")):
    if 1 <= unit_cost <= 6:
        cursor = collection.find({'cost': unit_cost}, {'_id': 0})
        if cursor:
            json_results = json_util.dumps(cursor, default=json_encoder)
            return json_results
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit cost not found")


@app.get("/units/traits/{unit_traits}")
async def get_units_by_traits(unit_traits: str = Path(..., description="The trait of the units you want to retrieve"),
                              s1: str = Query(None),
                              s2: str = Query(None),
                              s3: str = Query(None)):
    subtraits = [trait for trait in [s1, s2, s3] if trait is not None]

    query = {"traits": {"$all": [unit_traits, *subtraits]}} if subtraits else {"traits": unit_traits}

    cursor = collection.find(query, {'_id': 0})
    if cursor:
        json_results = json_util.dumps(cursor, default=json_encoder)
        if json_results != "[]":
            return json_results
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit traits not found")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit traits not found")


@app.post("/add_unit/{new_card_id}}", include_in_schema=False)  # POST - METHOD to add a new unit
async def add_unit(new_card_id: int, card: Card):
    cursor = collection.find({'id': new_card_id})
    if cursor:
        json_results = json_util.dumps(cursor, default=json_encoder)
        if json_results != "[]":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Couldn't insert Card with id: {new_card_id}. Maybe it already exists?")
        else:
            card = dict(card)
            result = collection.insert_one(card)
            if result.inserted_id == 1:
                return {'message': f'New card wtih id {new_card_id} added!'}, card
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Inserction of Card with id: {new_card_id} failed.")


@app.delete("/delete_unit/{card_id}}", include_in_schema=False)  # DELETE - METHOD to delete a new unit
async def delete_unit(card_id: int):
    result = collection.find_one_and_delete({"id": card_id})
    if result:
        return {'message': f'Card with id {card_id} successfully deleted.'}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Deletion of Card with id: {card_id} failed.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
