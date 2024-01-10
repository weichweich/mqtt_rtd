# MQTT RTD

Read temperature and publish them via MQTT for [Home Assistant](https://github.com/home-assistant/core).

* Read temperature using [adafruit MAX31865](https://www.adafruit.com/product/3328) and a PT100/PT1000
* Publish sensor readings using MQTT
* Support Home Assistant auto discovery

## Setup

* Install [poetry](https://github.com/python-poetry/poetry)
* Clone this repository
* Install dependencies with `poetry install -E embedded`
    * with `-E embedded` if MAX31865 is attached via SPI
    * without `embedded` if no sensors are connected
