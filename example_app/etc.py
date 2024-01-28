from pathlib import Path


def app_resource(path: str):
    return Path(__file__).parent / path
