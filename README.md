patent-parsing-tools
====================

## System requirements:

  sudo yum install python-devel libxslt-devel libxml2-devel

## Python requirements:

  pip install -r requirements.txt

## Running:

  python -m patent_parsing_tools.supervisor [working_directory] [train_destination] [test_destination] [year_from] [year_to]

## Running tests

  python -m unittest discover .

