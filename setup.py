#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Charles on 2018/6/20
# Function: setup log_config

from setuptools import setup, find_packages

setup(
    name='log_config',
    version="2.0",
    description=(
        "Provide a function for anyone who want to configure log parameters easily, just call init_log_config when your app start up, the you can use the module of logging which build-in python3 without any other configtur. This module support ConsoleHandler, RotatingFileHandler and SMTPHandler and You can change the configuration parameters according to your requirements."
    ),
    long_description=open('README.rst').read(),
    author='Wu Charles',
    author_email='wcadaydayup@163.com',
    maintainer='Wu Charles',
    maintainer_email='wcadaydayup@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/wcadaydayup/log_config/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
