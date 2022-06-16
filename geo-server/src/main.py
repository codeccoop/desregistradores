# BUILT-INS
from typing import Dict, Optional

# VENDOR
from fastapi import FastAPI, Response

# SOURCE
from src.db import models, queries, serializer, client as db_cli

app = FastAPI()
MEDIA_TYPE = "application/json; charset=utf-8"


@app.get("/")
async def root() -> Dict[str, str]:
    return {"status": "Hello, world!"}


@app.get("/districtes")
async def get_districtes() -> Response:
    query = queries.districtes()
    data = db_cli.query(query)
    return Response(content=serializer.feature_collection(data), media_type=MEDIA_TYPE)


@app.post("/districtes")
async def post_districtes(bbox: models.BBox) -> Response:
    query = queries.districtes(bbox=bbox)
    data = db_cli.query(query)
    return Response(content=serializer.feature_collection(data), media_type=MEDIA_TYPE)


@app.get("/districtes/{id}")
async def get_districte(id: int) -> Response:
    query = queries.districtes(id=id)
    data = db_cli.query(query, many=False)
    return Response(content=serializer.feature(data), media_type=MEDIA_TYPE)


@app.get("/barris")
async def get_barris() -> Response:
    query = queries.barris()
    data = db_cli.query(query)
    return Response(content=serializer.feature_collection(data), media_type=MEDIA_TYPE)


@app.post("/barris")
async def post_barris(bbox: Optional[models.BBox]) -> Response:
    query = queries.barris(bbox=bbox)
    res = db_cli.execute(query)
    return Response(content=serializer.feature_collection(res), media_type=MEDIA_TYPE)


@app.get("/barris/{id}")
async def get_barri(id: int) -> Response:
    query = queries.barris(id=id)
    data = db_cli.query(query, many=False)
    return Response(content=serializer.feature(data), media_type=MEDIA_TYPE)


@app.get("/parceles")
async def get_parceles() -> Response:
    query = queries.parceles()
    data = db_cli.query(query)
    return Response(content=serializer.feature_collection(data), media_type=MEDIA_TYPE)


@app.post("/parceles")
async def post_parceles(bbox: Optional[models.BBox]) -> Response:
    query = queries.parceles(bbox=bbox)
    data = db_cli.query(query)
    return Response(content=serializer.feature_collection(data), media_type=MEDIA_TYPE)


@app.get("/parceles/{id}")
async def get_parcela(id: int) -> Response:
    query = queries.parceles(id=id)
    data = db_cli.query(query, many=False)
    return Response(content=serializer.feature(data), media_type=MEDIA_TYPE)
