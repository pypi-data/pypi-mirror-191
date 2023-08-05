from setuptools import setup, find_packages


setup(
    name="zs_base_api",
    version="0.0.1",
    author="Zonesmart",
    author_email="kamil@zonesmart.ru",
    packages=find_packages(include=["zs_base_api", "zs_base_api.*"]),
)
