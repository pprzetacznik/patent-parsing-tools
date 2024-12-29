#!/bin/sh

python -m nltk.downloader stopwords
pytest -m pytest \
  patent_parsing_tools \
  --cov-report term \
  --cov=patent_parsing_tools \
  --doctest-modules \
  -svvv
