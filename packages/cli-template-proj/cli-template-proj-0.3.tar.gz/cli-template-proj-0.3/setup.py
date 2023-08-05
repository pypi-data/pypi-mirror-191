from setuptools import setup

setup(
    name="cli-template-proj",
    version="0.3",
    py_modules=["main"],
    entry_points={"console_scripts": ["cli-template-proj=main:main"]},
)
