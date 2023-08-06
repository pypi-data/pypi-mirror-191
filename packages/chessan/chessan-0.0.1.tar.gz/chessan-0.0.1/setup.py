from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="chessan",
    version="0.0.1",
    author="Hart Traveller",
    license="MIT",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["rich", "requests"],
)
