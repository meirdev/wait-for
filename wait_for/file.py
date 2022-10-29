import os


def file(path: str) -> bool:
    return os.path.exists(path)
