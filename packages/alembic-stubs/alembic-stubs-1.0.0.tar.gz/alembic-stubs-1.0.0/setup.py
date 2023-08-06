from setuptools import __version__
from setuptools import setup

if not int(__version__.partition(".")[0]) >= 47:
    raise RuntimeError("Setuptools >= 47 required. Found {}".format(__version__))

setup()
