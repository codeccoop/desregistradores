__all__ = ["query"]

# BUILT-INS
from typing import Optional
from os import getcwd, path

# VENDOR
import spatialite
from sqlite3 import Row

# CONFIG
from src.db import config


def query(q: str, many: Optional[bool] = True):
    cur = execute(q, commit=False)

    if many is True:
        return cur.fetchall()
    else:
        return cur.fetchone()


def execute(q: str, commit: bool = True) -> spatialite.Connection:
    conn = spatialite.connect(path.join(getcwd(), config.DB_PATH))
    conn.row_factory = Row
    cur = conn.execute(q)
    if commit is True:
        conn.commit()
    return cur
