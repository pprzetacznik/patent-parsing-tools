# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from pip.req import parse_requirements


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "patent-parsing-tools",
    version = "0.9",
    author = "Michal Dul, Piotr Przetacznik, Krzysztof Strojny",
    author_email = "piotr.przetacznik@gmail.com",
    description = ("patent-parsing-tools is a library providing tools for generating training and test set from Google's USPTO data helpful with for testing machine learning algorithms"),
    license = "MIT",
    keywords = "deeplearning dbn rbm rsm backpropagation precission recall",
    url = "https://bitbucket.org/ml-patents/patent-parsing-tools",
    packages=find_packages(exclude=['contrib', 'docs', 'tests', '*.tests']),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
    ],
    install_requires=required,
    package_data={
        'patent-grant-specification': ['doc/patent-grant-v44-2013-05-16'],
    },
    data_files=[('config', ['patent_parsing_tools/extractor_configuration.json'])]
)
