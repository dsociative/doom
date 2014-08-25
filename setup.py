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
        "http://github.com/dsociative/socket_server2/tarball/staging#egg"
        "=socket_server2",
        "http://github.com/dsociative/rmodel/tarball/staging#egg=rmodel"
    ],
    install_requires=[
        'ztest',
        'class_collector',
        'jinja2',
        'socket_server2',
        'rmodel',
        'pyzmq',
        'pytest',
        'mock'
    ],
    package_data={'doom': ['template/*.rst']},
    version='0.0.3'
)

