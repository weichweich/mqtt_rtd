from dataclasses import dataclass, field
import pathlib
import random
import string
import tomlkit
from typing import List, Optional

from marshmallow import Schema, post_dump, validate
import marshmallow_dataclass


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class BaseSchema(Schema):

    @post_dump
    def remove_skip_none(self, data, **kwargs):
        return {key: value for key, value in data.items() if not value is None}


@dataclass
class SensorConfig(BaseSchema):
    chip_select: int = field(
        metadata={"validate": validate.Range(min=0, max=40)})
    name: str
    ref_resistor: float = field(default=4300.0)
    update_interval: float = field(default=60)
    dummy: bool = field(default=False)


@dataclass
class MqttConfig(BaseSchema):
    hostname: str
    password: Optional[str] = field(metadata={"allow_none": False})
    username: Optional[str] = field(metadata={"allow_none": False})
    topic_prefix: str

    port: int = field(
        default=1883,
        metadata={"validate": validate.Range(min=0, max=2**16 - 1)})


@dataclass
class Config(BaseSchema):
    sensor: List[SensorConfig]
    mqtt: MqttConfig
    name: str = field(default="MQTT RTD")
    mqtt_ident: str = field(default_factory=lambda: randomword(15))
    ha_discovery_prefix: str = field(default="homeassistant")


def load(path: pathlib.Path) -> Config:
    with path.open("r") as f:
        in_data = f.read()
        raw_toml = tomlkit.loads(in_data)
    config_schema = marshmallow_dataclass.class_schema(Config)()

    config = config_schema.load(raw_toml)

    updated_config = config_schema.dump(config)

    if raw_toml != updated_config:
        # save the `mqtt_ident` so that we use the same entity persistently.
        print("updating config")
        str_updated_config = tomlkit.dumps(updated_config)
        with path.open("w") as f:
            f.write(str_updated_config)

    return config
