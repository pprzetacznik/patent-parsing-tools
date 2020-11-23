patent-parsing-tools
====================

[![Build Status](https://travis-ci.org/pprzetacznik/patent-parsing-tools.svg?branch=master)](https://travis-ci.org/pprzetacznik/patent-parsing-tools)
[![Documentation Status](https://readthedocs.org/projects/patent-parsing-tools/badge/?version=latest)](https://patent-parsing-tools.readthedocs.io/en/latest/?badge=latest)
![patent-parsing-tools CI](https://github.com/pprzetacznik/patent-parsing-tools/workflows/patent-parsing-tools%20CI/badge.svg)

## Documentation

[Read the docs](https://patent-parsing-tools.readthedocs.io/en/latest/)

## System requirements:

```Bash
sudo yum install python-devel libxslt-devel libxml2-devel
```

## Python requirements:

```Bash
pip install -r requirements.txt
```

## Running:

Collecting and serializing data:
```Bash
python -m patent_parsing_tools.supervisor [working_directory] [train_destination] [test_destination] [year_from] [year_to]
```

Eg.
```Bash
python -m patent_parsing_tools.supervisor patents/working_directory patents/train_destination patents/test_destination 2014 2015
```

Generating dictionary with train set:
```Bash
python -m patent_parsing_tools.bow.dictionary_maker [train_directory] [max_parsed_patents] [dict_max_size] [dictionary_name]
```

Eg.
```Bash
python -m patent_parsing_tools.bow.dictionary_maker patents/train_destination 1000000000 4096 dictionary.txt
```

Generate bag of words with train set and test set:
```Bash
python -m patent_parsing_tools.bow.bag_of_words [directory_with_serialized_patents] [destination_directory] [dictionary.txt] [package_size > 1024]
```

Eg.
```Bash
python -m patent_parsing_tools.bow.bag_of_words patents/train_destination patents/final_dataset_train dictionary.txt 1048576
python -m patent_parsing_tools.bow.bag_of_words patents/test_destination patents/final_dataset_test dictionary.txt 1048576
```

## Running tests

```Bash
python -m unittest discover .
```
