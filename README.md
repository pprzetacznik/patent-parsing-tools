patent-parsing-tools
====================

## System requirements:

  sudo yum install python-devel libxslt-devel libxml2-devel

## Python requirements:

  pip install -r requirements.txt

## Running:

Collecting and serializing data

  python -m patent_parsing_tools.supervisor [working_directory] [train_destination] [test_destination] [year_from] [year_to]

Generating dictionary with train set

  python -m patent_parsing_tools.bow.dictionary_maker patents/train_destination 1000000000 4096 dictionary.txt

Generate bag of words with train set and test set

  python -m patent_parsing_tools.bow.bag_of_words patents/train_destination patents/final_dataset_train dictionary.txt 1048576
  python -m patent_parsing_tools.bow.bag_of_words patents/test_destination patents/final_dataset_test dictionary.txt 1048576

## Running tests

  python -m unittest discover .

