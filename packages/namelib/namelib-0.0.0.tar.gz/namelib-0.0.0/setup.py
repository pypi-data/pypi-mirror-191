from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="namelib",
    version="0.0.0",
    author="Hart Traveller",
    url="https://github.com/harttraveller/namelib",
    license="MIT",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["names-dataset"],
)
