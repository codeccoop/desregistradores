# BUIT-INS
from typing import Optional

# VENDOR
import spatialite

# SOURCE
from src.db.models import BBox


def bbox_to_polygon(bbox: BBox) -> str:
    return """GeomFromText('POLYGON (({east} {north}, {east} {south}, {west} {south}, {west} {north}, {east} {north}))', 4326)""".format(
        **bbox
    )


def districtes(id: Optional[int] = None, bbox: Optional[BBox] = None) -> str:
    query = """
    SELECT
        id,
        districte,
        nom,
        AsGeoJSON(wkb_geometry) AS geometry
    FROM districtes
    """

    if id is not None:
        query += "WHERE id = %s" % id
    elif bbox is not None:
        query += "WHERE Intersects(wkb_geometry, %s)" % bbox_to_polygon(bbox)

    return query


def barris(id: Optional[int] = None, bbox: Optional[BBox] = None) -> str:
    query = """
    SELECT
        id,
        districte,
        nom,
        AsGeoJSON(wkb_geometry) AS geometry
    FROM barris
    """

    if id is not None:
        query += "WHERE id = %s" % id
    elif bbox is not None:
        query += "WHERE Intersects(wkb_geometry, %s)" % bbox_to_polygon(bbox)

    return query


def parceles(id: Optional[int] = None, bbox: Optional[BBox] = None) -> str:
    query = """
    SELECT
        id,
        refcat,
        AsGeoJSON(wkb_geometry) AS geometry
    FROM parceles
    """

    if id is not None:
        query += "WHERE id = %s" % id
    elif bbox is not None:
        query += "WHERE Intersects(wkb_geometry, %s)" % bbox_to_polygon(bbox)

    return query
