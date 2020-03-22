import re
from nltk import download
from nltk.corpus import stopwords
from stemming.porter2 import stem
from patent_parsing_tools.utils.log import log


@log
class WordCount:
    def __init__(self):
        download("stopwords")
        self.stopwords = stopwords.words("english")
        self.wordcount_dictionary = {}
        self.parse_regexp = re.compile(
            r"([0-9]*[a-zA-Z][a-zA-Z0-9]+)", re.DOTALL
        )

    def parse_text(self, text, wordcount_dictionary=None):
        """
        >>> wordcount = WordCount() #doctest: +ELLIPSIS
        [nltk_data] ...
        >>> wordcount.parse_text("a1a ma kota")
        {'ma': 1, 'a1a': 1, 'kota': 1}
        >>> wordcount.parse_text("a1a ma kota", {'a1a': 2, 'kota': 1})
        {'ma': 1, 'a1a': 3, 'kota': 2}
        """
        if not wordcount_dictionary:
            wordcount_dictionary = {}
        words = self.parse_regexp.findall(text)
        for word in words:
            new_word = stem(word.lower())
            if new_word not in self.stopwords:
                if new_word in wordcount_dictionary:
                    wordcount_dictionary[new_word] += 1
                else:
                    wordcount_dictionary[new_word] = 1
        return wordcount_dictionary
