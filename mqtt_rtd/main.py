import asyncio
from typing import List
import aiomqtt

from cli import get_args
from config import Config, load
from mqtt import publish_ha_config, publish_temperature
from sensor import Sensor, sensor_from_config


async def publish_loop(client: aiomqtt.Client, config, sensor: Sensor):
    await publish_ha_config(client, config, sensor.config)
    while True:
        # TODO: law of demeter
        await publish_temperature(client, config, sensor)
        await asyncio.sleep(sensor.config.update_interval)


async def start_all(config: Config, sensors: List[Sensor]):
    try:
        return await __unsafe_start_all(config, sensors)
    except aiomqtt.error.MqttConnectError as e:
        print("MQTT connection error:", e)
    except aiomqtt.error.MqttError as e:
        print("MQTT error:", e)


async def __unsafe_start_all(config: Config, sensors: List[Sensor]):
    async with aiomqtt.Client(config.mqtt.hostname,
                              port=config.mqtt.port,
                              username=config.mqtt.username,
                              password=config.mqtt.password) as client:
        tasks = [
            asyncio.create_task(publish_loop(client, config, sensor))
            for sensor in sensors
        ]

        # TODO: handle errors, interupts etc.
        _done, pending = await asyncio.wait(tasks)

        for pending_task in pending:
            pending_task.cancel()


def main():
    args = get_args()

    config = load(args.config)

    sensors = sensor_from_config(config.sensor)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_all(config, sensors))
    except KeyboardInterrupt:
        print("Recevied Keyboard Interrupt... shutting down")

