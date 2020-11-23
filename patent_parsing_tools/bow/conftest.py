import os
import pytest
from pkg_resources import resource_filename
from patent_parsing_tools.bow.bag_of_words import BagOfWords


@pytest.fixture(autouse=True)
def bag_of_words(doctest_namespace):
    dictionary = resource_filename(
        "patent_parsing_tools.bow.tests", "dictionary.txt"
    )
    doctest_namespace["bag_of_words"] = BagOfWords(dictionary)
    yield
    if os.path.isfile("./final_serialized_patent"):
        os.remove("./final_serialized_patent")
