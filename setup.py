#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='command',
    author='dsociative',
    author_email='admin@geektech.ru',
    packages=find_packages(),
    dependency_links=[
        "http://github.com/dsociative/ztest/tarball/master#egg=ztest-0.0.0",
    ],
    install_requires=[
        'ztest'
    ]
)

