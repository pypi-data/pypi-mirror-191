import os
import pathlib
import tomli
import importlib.metadata

try:
    with open(os.path.join(os.path.abspath(pathlib.Path(__file__).parent.parent), 'pyproject.toml'), 'rb') as f:
        t = tomli.load(f)

    __version__ = t['tool']['poetry']['version']
except FileNotFoundError: # Package is in a context where pyproject not available (e.g. pip installed)
    try:
        __version__ = importlib.metadata.version('sunpeek')
    except importlib.metadata.PackageNotFoundError:
        __version__ = os.environ['SUNPEEK_VERSION']
