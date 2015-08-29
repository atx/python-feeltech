#! /usr/bin/env python3

from distutils.core import setup

setup(
    name = "python-feeltech",
    version = "0.1",
    packages = ["feeltech"],
    description = "Python library for controlling FeelTech FY32xx waveform generators ",
    author = "Josef Gajdusek",
    author_email = "atx@atx.name",
    url = "https://github.com/atalax/python-feeltech",
    license = "MIT",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        ]
    )
