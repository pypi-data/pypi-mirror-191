import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
#README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Royal-102016082",
    version="2.0",
    description="Topsis Assignment",
    #long_description=README,
    #long_description_content_type="text/markdown",
    #url="https://github.com/uditvashisht/saral-square",
    author="Royal Garg",
    author_email="royalgarg36@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["topsis_assignment"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "topsis=topsis_assignment.__main__:main",
        ]
    },
)