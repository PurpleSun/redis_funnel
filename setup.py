#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 22:27
from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

setup(
    name="redis-funnel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="TBD",
    version="0.0.1",
    keywords=("distributed", "funnel", "redis"),
    description="A distributed funnel system based on redis, management system included.",
    license="MIT License",
    install_requires=["Flask==1.0.2", "redis==3.2.1"],
    author="fanwei.zeng",
    author_email="stayblank@gmail.com",
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    platforms="any"
)
