#!/bin/bash

set -xeuo pipefail

python -m nltk.downloader stopwords
python -m pytest \
  patent_parsing_tools \
  --cov-report term \
  --cov=patent_parsing_tools \
  --doctest-modules \
  -svvv
