import os
from os.path import join, dirname
from typing import Dict, Any

from dotenv import load_dotenv, find_dotenv


def get_config() -> Dict[str, Any]:
    load_dotenv(find_dotenv())

    return {'token': os.environ.get("TOKEN")}
