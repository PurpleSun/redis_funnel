#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 22:27
from setuptools import setup, find_packages

setup(
    name="redis-funnel",
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
    platforms="any",
)
