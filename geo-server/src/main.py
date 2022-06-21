# BUILT-INS
from typing import Dict, Optional

# VENDOR
from fastapi import FastAPI, Response

# SOURCE
from src.db import models, queries, serializer, client as db_cli

app = FastAPI()
MEDIA_TYPE = "application/json; charset=UTF-8"


@app.get("/")
async def root() -> Dict[str, str]:
    return {"status": "Hello, world!"}


@app.get("/districtes")
async def get_districtes(geom: bool = False) -> Response:
    query = queries.districtes(geom=geom)
    data = db_cli.query(query)
    if geom is True:
        return Response(
            content=serializer.feature_collection(data), media_type=MEDIA_TYPE
        )
    else:
        return Response(content=serializer.collection(data), media_type=MEDIA_TYPE)


@app.post("/districtes")
async def post_districtes(bbox: models.BBox, geom: bool = False) -> Response:
    query = queries.districtes(bbox=bbox, geom=geom)
    data = db_cli.query(query)
    if geom is True:
        return Response(
            content=serializer.feature_collection(data), media_type=MEDIA_TYPE
        )
    else:
        return Response(content=serializer.collection(data), media_type=MEDIA_TYPE)


@app.get("/districtes/{id}")
async def get_districte(id: int, geom: bool = False) -> Response:
    query = queries.districtes(id=id, geom=geom)
    data = db_cli.query(query, many=False)
    if geom is True:
        return Response(content=serializer.feature(data), media_type=MEDIA_TYPE)
    else:
        return Response(content=serializer.object(data), media_type=MEDIA_TYPE)


@app.get("/barris")
async def get_barris(geom: bool = False) -> Response:
    query = queries.barris(geom=geom)
    data = db_cli.query(query)
    if geom is True:
        return Response(
            content=serializer.feature_collection(data), media_type=MEDIA_TYPE
        )
    else:
        return Response(content=serializer.collection(data), media_type=MEDIA_TYPE)


@app.post("/barris")
async def post_barris(bbox: Optional[models.BBox], geom: bool = False) -> Response:
    query = queries.barris(bbox=bbox, geom=geom)
    data = db_cli.execute(query)
    if geom is True:
        return Response(
            content=serializer.feature_collection(data), media_type=MEDIA_TYPE
        )
    else:
        return Response(content=serializer.collection(data), media_type=MEDIA_TYPE)


@app.get("/barris/{id}")
async def get_barri(id: int, geom: bool = False) -> Response:
    query = queries.barris(id=id, geom=geom)
    data = db_cli.query(query, many=False)
    if geom is True:
        return Response(content=serializer.feature(data), media_type=MEDIA_TYPE)
    else:
        return Response(content=serializer.object(data), media_type=MEDIA_TYPE)


@app.get("/parceles")
async def get_parceles(geom: bool = False) -> Response:
    query = queries.parceles(geom=geom)
    data = db_cli.query(query)
    if geom is True:
        return Response(
            content=serializer.feature_collection(data), media_type=MEDIA_TYPE
        )
    else:
        return Response(content=serializer.collection(data), media_type=MEDIA_TYPE)


@app.post("/parceles")
async def post_parceles(bbox: Optional[models.BBox], geom: bool = False) -> Response:
    query = queries.parceles(bbox=bbox, geom=geom)
    data = db_cli.query(query)
    if geom is True:
        return Response(
            content=serializer.feature_collection(data), media_type=MEDIA_TYPE
        )
    else:
        return Response(content=serializer.collection(data), media_type=MEDIA_TYPE)


@app.get("/parceles/{refcat}")
async def get_parcela(refcat: str, geom: bool = False) -> Response:
    query = queries.parceles(refcat=refcat, geom=geom)
    data = db_cli.query(query, many=False)
    if geom is True:
        return Response(content=serializer.feature(data), media_type=MEDIA_TYPE)
    else:
        return Response(content=serializer.object(data), media_type=MEDIA_TYPE)


@app.put("/parceles/{refcat}")
async def put_parcela(refcat: str, note: models.Note) -> Dict[str, bool]:
    query = queries.update_parcela(refcat=refcat, note_id=note.note_id)
    db_cli.execute(query)
    return {"success": True}
