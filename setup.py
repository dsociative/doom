#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='doom',
    author='dsociative',
    author_email='admin@geektech.ru',
    packages=find_packages(),
    dependency_links=[
        "http://github.com/dsociative/ztest/tarball/master#egg=ztest-0.0.0",
        "http://github.com/dsociative/class_collector/tarball/master#egg"
        "=class_collector",
    ],
    install_requires=[
        'ztest',
        'class_collector',
        'jinja2'
    ],
    package_data={'doom': ['template/*.rst']},
)

