import argparse
import pathlib


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config",
                        type=pathlib.Path,
                        help="Path to the configuration file.",
                        required=True)

    parser.add_argument(
        "--mock",
        action="store_true",
        help="Son't use a real SPI interface, useful for testing.")

    return parser.parse_args()
