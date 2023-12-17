from dataclasses import dataclass, field
import pathlib
import random
import string
import tomllib
from typing import List, Optional

from marshmallow import validate
import marshmallow_dataclass


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@dataclass
class SensorConfig:
    chip_select: int = field(
        metadata={"validate": validate.Range(min=0, max=40)})
    name: str
    ref_resistor: float = field(default=4300.0)
    update_interval: float = field(default=60)
    dummy: bool = field(default=False)


@dataclass
class MqttConfig:
    hostname: str
    password: Optional[str]
    username: Optional[str]

    port: int = field(
        default=1883,
        metadata={"validate": validate.Range(min=0, max=2**16 - 1)})


@dataclass
class Config:
    sensor: List[SensorConfig]
    mqtt: MqttConfig
    name: str = field(default="MQTT RTD")
    mqtt_ident: str = field(default_factory=lambda: randomword(15))
    ha_discovery_prefix: str = field(default="homeassistant")


def load(path: pathlib.Path) -> Config:
    with path.open("rb") as f:
        raw_toml = tomllib.load(f)
    config_schema = marshmallow_dataclass.class_schema(Config)()

    return config_schema.load(raw_toml)
