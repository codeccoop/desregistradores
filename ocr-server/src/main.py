# BUILT-INS
import os.path
from os import getcwd
from typing import Dict
import time

# VENDOR
import aiofiles
from fastapi import FastAPI, Response, UploadFile, File

# SOURCE
from .config import TMP_DIRECTORY
from src.parsers.pdf import PdfParser
from src.parsers.geocoding import GeoLocation


app = FastAPI()


@app.get("/")
async def root() -> Dict[str, str]:
    return {"status": "Hello World!"}


@app.post("/note")
async def post_note(file: bytes = File()):
    filename = str(round(time.time()))
    filepath = os.path.abspath(os.path.join(TMP_DIRECTORY, filename))
    async with aiofiles.open(filepath, "wb") as f:
        await f.write(file)

    parser = PdfParser(filepath)
    GeoLocation(parser)
    fmt = parser.format
    data = parser.data
    return {
        "format": fmt,
        **data.description.data,
        **data.ownership.data,
        **parser.geolocation.data,
    }
