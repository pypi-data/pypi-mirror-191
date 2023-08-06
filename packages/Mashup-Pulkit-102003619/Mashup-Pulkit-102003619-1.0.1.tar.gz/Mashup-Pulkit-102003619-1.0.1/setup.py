import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Mashup-Pulkit-102003619",
    version="1.0.1",
    description="A Python program that allows user to create mashup of audios which are extracted from youtube videos requested singer",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Pulkit0103",
    author="Pulkit",
    author_email="girdhar.pulkit.2002@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    packages=["mashup"],
    include_package_data=True,
    install_requires=['pathlib',
                      'numpy',
                      'pandas',
                      'pydub',
                      'pytube'],
    entry_points={
        "console_scripts": [
            "mashup=mashup.__main__:main",
        ]
    },
)