# BUILT-INS
from typing import Optional

# VENDOR
from fastapi import FastAPI

# SOURCE
from src.db import models, queries, serializer, client as db_cli

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "Hello, world!"}


@app.get("/districtes")
async def get_districtes() -> models.FeatureCollection:
    query = queries.districtes()
    data = db_cli.query(query)
    print(data)
    return serializer.feature_collection(data)


@app.post("/districtes")
async def post_districtes(bbox: models.BBox) -> models.Districtes:
    query = queries.districtes(bbox=bbox)
    data = db_cli.query(query)
    return serializer.feature_collection(data)


@app.get("/districtes/{id}")
async def get_districte(id: int) -> models.Feature:
    query = queries.districtes(id=id)
    data = db_cli.query(query, many=False)
    return serializer.feature(data)


@app.get("/barris")
async def get_barris() -> models.Barris:
    query = queries.barris()
    data = db_cli.query(query)
    return serializer.feature_collection(data)


@app.post("/barris")
async def post_barris(bbox: Optional[models.BBox]) -> models.Barris:
    query = queries.barris(bbox=bbox)
    res = db_cli.execute(query)
    return serializer.feature_collection(res)


@app.get("/barris/{id}")
async def get_barri(id: int) -> models.Feature:
    query = queries.barris(id=id)
    data = db_cli.query(query, many=False)
    return serializer.feature(data)


@app.get("/parceles")
async def get_parceles() -> models.Parceles:
    query = queries.parceles()
    data = db_cli.query(query)
    return serializer.feature_collection(data)


@app.post("/parceles")
async def post_parceles(bbox: Optional[models.BBox]) -> models.Parceles:
    query = queries.parceles(bbox=bbox)
    data = db_cli.query(query)
    return serializer.feature_collection(data)


@app.get("/parceles/{id}")
async def get_parcela(id: int) -> models.Feature:
    query = queries.parceles(id=id)
    data = db_cli.execute(query, many=False)
    return serializer.feature(data)
