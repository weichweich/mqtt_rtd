from dataclasses import dataclass, field
import pathlib
import tomllib
from typing import List

from marshmallow import validate
import marshmallow_dataclass


@dataclass
class Sensor:
    chip_select: int = field(
        metadata={"validate": validate.Range(min=0, max=40)})
    name: str


@dataclass
class Config:
    sensor: List[Sensor]
    ha_discovery_prefix: str = field(default="homeassistant")


def load(path: pathlib.Path) -> Config:
    with path.open("rb") as f:
        raw_toml = tomllib.load(f)
    config_schema = marshmallow_dataclass.class_schema(Config)()

    return config_schema.load(raw_toml)
