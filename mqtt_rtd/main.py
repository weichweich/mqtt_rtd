from cli import get_args
from config import load


def main():
    args = get_args()

    config = load(args.config)

    print(config)
