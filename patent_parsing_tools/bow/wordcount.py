import re
from nltk import download
from nltk.corpus import stopwords
from stemming.porter2 import stem


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
        >>> wordcount = WordCount()
        >>> wordcount.parse_text("a1a m4 kota")
        {'a1a': 1, 'm4': 1, 'kota': 1}
        >>> wordcount.parse_text("a1a m4 kota", {'a1a': 2, 'kota': 1})
        {'a1a': 3, 'kota': 2, 'm4': 1}
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
