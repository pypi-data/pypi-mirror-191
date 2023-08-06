"""Testing python packaging"""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    pass


def describe() -> str:
    return "A package testing python packaging."
