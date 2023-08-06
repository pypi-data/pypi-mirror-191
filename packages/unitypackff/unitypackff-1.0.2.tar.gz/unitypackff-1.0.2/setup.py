#!/usr/bin/env python3

from setuptools import setup


setup(
    long_description=open("README.md","r",encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    project_urls={
        "GitHub": "https://github.com/SirDank/UnityPackFF",
        "Bug Tracker": "https://github.com/SirDank/UnityPackFF/issues",
    },
    license="MIT",
    package_dir={"": "."},
    keywords=["unity","unitypack","unitypackff"],
)
