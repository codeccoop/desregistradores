# BUILT-INS
import json

# SOURCE
from .models import FeatureCollection, Feature


def feature_collection(data: list) -> FeatureCollection:
    return FeatureCollection(
        **{
            "type": "FeatureCollection",
            "features": [
                Feature(
                    **{
                        "properties": {
                            key: item[key] for key in item.keys() if key != "geometry"
                        },
                        "geometry": json.loads(item["geometry"]),
                    }
                )
                for item in data
            ],
        }
    )


def feature(data: dict) -> Feature:
    return Feature(
        **{
            "properties": {key: data[key] for key in data if key != "geometry"},
            "geometry": json.loads(data["geometry"]),
        }
    )
