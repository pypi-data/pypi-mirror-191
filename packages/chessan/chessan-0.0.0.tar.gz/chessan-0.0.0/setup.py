from setuptools import setup, find_packages

setup(
    name="chessan",
    version="0.0.0",
    author="Hart Traveller",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["rich", "requests"],
)
