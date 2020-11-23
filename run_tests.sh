#!/bin/sh

python -m nltk.downloader stopwords
python -m unittest discover .
