import pathlib
from setuptools import setup, find_packages


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="gretzky_ovi", packages=find_packages(),
)
