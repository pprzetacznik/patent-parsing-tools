import os
from setuptools import setup, find_packages


with open("requirements.txt") as f:
    required = f.read().splitlines()


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="patent-parsing-tools",
    version="0.9.3",
    author="Michal Dul, Piotr Przetacznik, Krzysztof Strojny",
    author_email="piotr.przetacznik@gmail.com",
    description=(
        "patent-parsing-tools is a library providing tools for generating"
        " training and test set from Google's USPTO data helpful with for"
        " testing machine learning algorithms"
    ),
    license="MIT",
    keywords="deeplearning dbn rbm rsm backpropagation precission recall",
    url="https://github.com/pprzetacznik/patent-parsing-tools",
    packages=find_packages(),
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    package_data={"": ["*.txt", "*.json", "*.XML"]},
    install_requires=required,
)
