# VENDOR
import geocoder

# BUILT-INS
import re
import json

# SOURCE
from src.parsers.numeric import Numeric


def parse_street(chars):
    if not chars:
        return ""

    street = " ".join(
        [
            chunk.lower()
            for word in chars.split(" ")
            for chunk in re.split(r"([A-Z][a-z]+)", word)
            if chunk
        ]
    )
    return street


def parse_town(chars):
    if not chars:
        return ""

    town = " ".join(
        [
            chunk.lower()
            for word in chars.split(" ")
            for chunk in re.split(r"([A-Z][a-z]+)", word)
            if chunk
        ]
    )
    town = re.sub(r"(villa|vila)( *de *)?", "", town)
    return town


def build_address(record):
    data = record.description.data
    address = "{number} {street}, {town}, cataluña, españa".format(
        number=Numeric(data.get("number")),
        street=parse_street(data.get("street")),
        town=parse_town(data.get("town")),
    )

    address = re.sub(r"^ *, *", "", re.sub(r"(?<=,) *,", "", address))
    return address


class GeoLocation(object):
    def __init__(self, parser):
        self._data = self.geolocate(parser.data).json or {}
        setattr(parser, "geolocation", self)

    def geolocate(self, record):
        address = build_address(record)
        res = geocoder.osm(address)
        return res

    @property
    def latlng(self):
        return [self._data.get("lat"), self._data.get("lng")]

    @property
    def address(self):
        return self._data.get("address")

    @property
    def street(self):
        return self._data.get("street")

    @property
    def postcode(self):
        return self._data.get("postcode")

    @property
    def town(self):
        return self._data.get("town")

    @property
    def county(self):
        return self._data.get("county")

    @property
    def region(self):
        return self._data.get("region")

    @property
    def country(self):
        return self._data.get("country")

    @property
    def data(self):
        return {
            "latlng": self.latlng,
            "street": self.street,
            "postcode": self.postcode,
            "town": self.town,
            "county": self.county,
            "region": self.region,
            "country": self.country,
            "address": self.address,
        }

    def __str__(self):
        return json.dumps(self.data)
