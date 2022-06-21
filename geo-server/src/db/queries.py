# BUIT-INS
from typing import Optional

# VENDOR
import spatialite

# SOURCE
from src.db.models import BBox


def bbox_to_polygon(bbox: BBox) -> str:
    return """GeomFromText('POLYGON (({east} {north}, {east} {south}, {west} {south}, {west} {north}, {east} {north}))', 4326)""".format(
        **dict(bbox)
    )


def districtes(
    id: Optional[int] = None, bbox: Optional[BBox] = None, geom: bool = True
) -> str:
    query = """
    SELECT
        id,
        nom"""

    if geom is True:
        query += """,
        AsGeoJSON(geometry) AS geometry"""

    query += """
    FROM districtes
    """

    if id is not None:
        query += "WHERE id = %s" % id
    elif bbox is not None:
        query += "WHERE Intersects(geometry, %s)" % bbox_to_polygon(bbox)

    return query


def barris(
    id: Optional[int] = None, bbox: Optional[BBox] = None, geom: bool = True
) -> str:
    query = """
    SELECT
        id,
        districte,
        nom"""

    if geom is True:
        query += """,
        AsGeoJSON(geometry) AS geometry"""

    query += """
    FROM barris
    """

    if id is not None:
        query += "WHERE id = %s" % id
    elif bbox is not None:
        query += "WHERE Intersects(geometry, %s)" % bbox_to_polygon(bbox)

    return query


def parceles(
    refcat: Optional[str] = None, bbox: Optional[BBox] = None, geom: bool = True
) -> str:
    query = """
    SELECT
        ogc_fid AS id,
        refcat,
        barri,
        districte,
        note_id"""

    if geom is True:
        query += """,
        AsGeoJSON(geometry) AS geometry"""

    query += """
    FROM parceles
    """

    if refcat is not None:
        query += "WHERE refcat = '%s'" % refcat
    elif bbox is not None:
        query += "WHERE Intersects(geometry, %s)" % bbox_to_polygon(bbox)

    return query


def update_parcela(refcat: str, note_id: int) -> str:
    query = f"""
    UPDATE parceles
    SET note_id = {note_id}
    WHERE refcat = '{refcat}'
    """

    print(query)
    return query
