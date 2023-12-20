import json
import aiomqtt

from config import Config, SensorConfig
from connectivity import get_ip
from sensor import Sensor


def state_topic(config: Config, sensor: SensorConfig) -> str:
    return f"{config.mqtt.topic_prefix}/sensor/{sensor.name}"


async def publish_temperature(client: aiomqtt.Client, config: Config,
                              sensor: Sensor):
    await client.publish(state_topic(config, sensor.config),
                         payload=json.dumps(
                             {"temperature": sensor.temperature()}))


async def publish_ha_config(client: aiomqtt.Client, config: Config,
                            sensor: SensorConfig):
    payload = {
        "device_class": "temperature",
        "native_unit_of_measurement": "°C",
        "value_template": "{{ value_json.temperature}}",
        "name": sensor.name,
        "device": {
            "name": config.name,
            "identifiers": ["mqtt-rtd", config.mqtt_ident],
        },
        "unique_id": f"{config.mqtt_ident}_temp_{sensor.name}",
        "state_topic": state_topic(config, sensor),
        "state_class": "measurement",
        "connections": [["IP", get_ip()]],
        "suggested_display_precision": 2,
    }

    await client.publish(
        f"{config.ha_discovery_prefix}/sensor/{config.mqtt_ident}/{sensor.name}/config",
        payload=json.dumps(payload),
        retain=True)
