from dataclasses import dataclass
from pathlib import Path
from os import getenv
from dotenv import load_dotenv

origin_path = Path(__file__).parent.parent.resolve()


@dataclass
class FilePathTo:
    Queries = f"{origin_path.joinpath('resources','queries.json')}"


@dataclass
class FlaskConfig:
    Host: str = '0.0.0.0'
    Port: int = 5001


@dataclass
class EnvVar:
    load_dotenv()
    REGION_NAME = getenv("REGION_NAME")
    CLIENT_ID = getenv("CLIENT_ID")
    SECRET_HASH = getenv("SECRET_HASH")
