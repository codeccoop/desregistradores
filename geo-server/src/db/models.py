# BUILT-INS
from typing import List, Dict, Any

# VENDOR
from pydantic import BaseModel


class BBox(BaseModel):
    west: float
    south: float
    east: float
    north: float


class Geometry(BaseModel):
    type: str = "Polygon"
    coordinates: list


class Feature(BaseModel):
    geometry: Geometry
    properties: Dict[str, Any]


class FeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[Feature]


class Districteproperties(BaseModel):
    id: int
    nom: str


class Districte(Feature):
    pass


class Districtes(FeatureCollection):
    features: List[Districte]


class BarriProperties(BaseModel):
    id: int
    nom: str
    districtre: str


class Barri(Feature):
    pass


class Barris(FeatureCollection):
    features: List[Barri]


class ParcelaProperties(BaseModel):
    id: int
    refcat: str
    districte: int
    barri: int
    note_id: int


class Note(BaseModel):
    note_id: int


class Parcela(Feature):
    pass


class Parceles(FeatureCollection):
    features: List[Parcela]
