import io
from setuptools import setup

with io.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

tests_require = ["pytest", "pytest-cov", "Faker", "mock"]

setup(
    # Package
    name="dsconfig",
    version="1.6.6",
    author="KITS",
    author_email="kits-sw@maxiv.lu.se",
    url="https://gitlab.com/MaxIV/lib-maxiv-dsconfig",
    license="GPLv3",
    packages=["dsconfig", "dsconfig.appending_dict"],
    description="Library and utilities for Tango device configuration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Tango",
    # Requirements
    python_requires=">=2.7",
    install_requires=["jsonpatch>=1.13", "jsonschema", "six", "xlrd", "pytango"],
    extras_require={"tests": tests_require},
    # Resources
    package_data={"dsconfig": ["schema/dsconfig.json", "schema/schema2.json"]},
    # Scripts
    entry_points={
        "console_scripts": [
            "xls2json = dsconfig.excel:main",
            "json2tango = dsconfig.json2tango:main",
        ]
    },
)
