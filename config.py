from typing import List
import os
import json
from functools import lru_cache

from pydantic import BaseModel

from models import Team

class ServerConfig(BaseModel):
    version: str
    teams: List[Team]

@lru_cache()
def server_config():
    fname = os.environ['INDY_CONFIG']
    with open(fname, encoding='utf-8') as f:
        data = json.load(f)
    return ServerConfig(**data)

