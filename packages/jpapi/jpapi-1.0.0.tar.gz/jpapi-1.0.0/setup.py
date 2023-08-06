from setuptools import setup, find_packages
from version import __version__

setup(
    name="jpapi",
    packages=find_packages(),
    version=__version__,
    license="LGPLv3",
    description="A simple JSON API system for python",
    author="eb3095",
    author_email="ebennerit@gmail.com",
    url="https://github.com/eb3095/jpapi",
    keywords=["api", "jpapi", "python"]
)
