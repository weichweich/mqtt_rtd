from typing import List

from config import SensorConfig


class Sensor:
    config: SensorConfig

    def __init__(self, config: SensorConfig) -> None:
        self.config = config

    def temperature(self) -> float:
        raise NotImplementedError


class DummySensor(Sensor):
    """For testing without a sensor.
    """
    def temperature(self) -> float:
        return 0.0


class AdafruitSensor(Sensor):
    spi = None

    def __init__(self, config: SensorConfig) -> None:
        super().__init__(config)
        import board
        import digitalio
        import adafruit_max31865
        from adafruit_blinka.agnostic import board_id, detector

        def int_to_board(pin_number: int):
            match pin_number:
                case 5:
                    return board.D5
                case 6:
                    return board.D6

        if detector.board.any_embedded_linux:
            print("Running on embedded linux")

        if self.__class__.spi is None:
            self.__class__.spi = board.SPI()

        self.cs = digitalio.DigitalInOut(int_to_board(config.chip_select))
        self.sensor = adafruit_max31865.MAX31865(
            self.__class__.spi,
            self.cs,
            rtd_nominal=1000.0,
            ref_resistor=config.ref_resistor)


    def temperature(self) -> float:
        return self.sensor.temperature

def sensor_from_config(sensor_config: List[SensorConfig]) -> List[DummySensor]:
    sensors = []
    for config in sensor_config:
        if config.dummy:
            sensors.append(DummySensor(config))
        else:
            sensors.append(AdafruitSensor(config))
    return sensors
