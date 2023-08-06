from setuptools import setup

setup(
    name="maia-cli",
    version="0.3.1",
    py_modules=["main"],
    entry_points={"console_scripts": ["maia-cli=main:main"]},
)
