# BUILT-INS
import json
from typing import List

# SOURCE
from sqlite3 import Row


def feature_collection(data: List[Row]) -> str:
    return '{"type":"FeatureCollection","features":[%s]}' % (
        ",".join([feature(item) for item in data]),
    )


def feature(data: Row):
    return '{"type":"Feature","properties":%s,"geometry":%s}' % (
        json.dumps({key: data[key] for key in data.keys() if key != "geometry"}),
        data["geometry"],
    )
