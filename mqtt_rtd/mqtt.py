import json
import aiomqtt

from config import Config, SensorConfig


async def publish_temperature(client: aiomqtt.Client, topic: str,
                              temperature: float):
    await client.publish(topic, payload=json.dumps({"temperature": temperature}))


async def publish_ha_config(client: aiomqtt.Client, config: Config,
                            sensor: SensorConfig):
    payload = {
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "value_template": "{{ value_json.temperature}}",
        "name": sensor.name,
        "device": {
            "name": config.name,
            "identifiers": ["mqtt-rtd", config.mqtt_ident],
        },
        "unique_id": f"{config.mqtt_ident}_temp_{sensor.name}",
        "state_topic": 
    }

    await client.publish(
        f"{config.ha_discovery_prefix}/sensor/{config.mqtt_ident}/{sensor.name}/config",
        payload=json.dumps(payload),
        retain=True)
