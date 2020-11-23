#!/bin/sh

python -m nltk.downloader stopwords
pytest patent_parsing_tools --doctest-modules -s
