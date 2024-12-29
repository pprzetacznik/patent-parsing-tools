patent-parsing-tools
====================
USPTO patents dataset generator.

[![Documentation Status](https://readthedocs.org/projects/patent-parsing-tools/badge/?version=latest)](https://patent-parsing-tools.readthedocs.io/en/latest/?badge=latest)
[![patent-parsing-tools CI](https://github.com/pprzetacznik/patent-parsing-tools/workflows/patent-parsing-tools%20CI/badge.svg)](https://github.com/pprzetacznik/patent-parsing-tools/actions?query=workflow%3A"patent-parsing-tools+CI")
[![PyPI version](https://badge.fury.io/py/patent-parsing-tools.svg)](https://pypi.org/project/patent-parsing-tools/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/patent-parsing-tools)](https://pypi.org/project/patent-parsing-tools/)

## Documentation

[Read the docs](https://patent-parsing-tools.readthedocs.io/en/latest/)

## System requirements

```Bash
sudo yum install python-devel libxslt-devel libxml2-devel
```

## Installation:

```
pip install patent-parsing-tools
```

## Examples:

Downloading dataset:
```Bash
python -m patent_parsing_tools.downloader \
  --directory dataset \
  --year-from 2010 \
  --year-to 2010
```

Collecting and serializing data:
```Bash
python -m patent_parsing_tools.supervisor \
  --working-directory patents/working_directory \
  --train-destination patents/train_destination \
  --test-destination patents/test_destination \
  --year-from 2014 \
  --year-to 2015
```

Generating dictionary with train set:
```Bash
python -m patent_parsing_tools.bow.dictionary_maker \
  --train-directory patents/train_destination \
  --max-patents 1000000000 \
  --dictionary dictionary.txt \
  --dict-max-size 4096
```

Generate bag of words with train set and test set:
```Bash
python -m patent_parsing_tools.bow.bag_of_words \
  --serialized-patents patents/train_destination \
  --destination-directory patents/final_dataset_train \
  --dictionary dictionary.txt \
  --batch-size 1048576
python -m patent_parsing_tools.bow.bag_of_words \
  --serialized-patents patents/test_destination \
  --destination-directory patents/final_dataset_test \
  --dictionary dictionary.txt \
  --batch-size 1048576
```

## Testing

```Bash
pytest
```

## Contributing and develpment

```Bash
$ mkvirtualenv ppt
$ workon ppt
(ppt) $ pip install -r requirements.txt
```

## Publish new release

```Bash
$ git tag v1.0
$ git push origin v1.0
```

## Building documentation

```Bash
(ppt) $ sphinx-build -M html docs docs_build
```

## References

Usage:
* Elton, *Using natural language processing techniques to extract information on the properties and functionalities of energetic materials from large text corpora*, 2019, online: [https://arxiv.org/abs/1903.00415](https://arxiv.org/abs/1903.00415).
* Lee, *Natural Language Processing Techniques for Advancing Materials Discovery: A Short Review*, 2023, online: [https://doi.org/10.1007/s40684-023-00523-6](https://doi.org/10.1007/s40684-023-00523-6).

## License

The MIT License (MIT). Copyright (c) 2014 Michał Dul, Piotr Przetacznik, Krzysztof Strojny. Check [LICENSE](LICENSE) files for more information.

