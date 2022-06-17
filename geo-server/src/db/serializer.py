# BUILT-INS
import json
from typing import List

# SOURCE
from sqlite3 import Row


def feature_collection(data: List[Row]) -> str:
    return '{"type":"FeatureCollection","features":[%s]}' % (
        ",".join([feature(item) for item in data]),
    )


def feature(data: Row) -> str:
    return '{"type":"Feature","properties":%s,"geometry":%s}' % (
        json.dumps(
            {key: data[key] for key in data.keys() if key != "geometry"},
            ensure_ascii=False,
        ),
        data["geometry"],
    )


def collection(data: List[Row]) -> str:
    return "[" + ",".join([object(row) for row in data]) + "]"


def object(data: Row) -> str:
    return json.dumps({key: data[key] for key in data.keys()}, ensure_ascii=False)
