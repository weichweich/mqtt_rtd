

def init_sensor(chip_select: int):
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

    spi = board.SPI()
    cs = digitalio.DigitalInOut(
        int_to_board(chip_select))  # Chip select of the MAX31865 board.
    sensor = adafruit_max31865.MAX31865(spi,
                                        cs,
                                        rtd_nominal=1000.0,
                                        ref_resistor=4300.0)
    return sensor

def init_dummy(chip_select: int):
    return DummySensor()

class DummySensor:
    @property
    def temperature():
        return 0
