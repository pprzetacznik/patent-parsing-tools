import os
import sys
import pickle
from pkg_resources import resource_filename
from patent_parsing_tools.supervisor import Supervisor
from patent_parsing_tools.bow.wordcount import WordCount
from patent_parsing_tools.utils.log import log, log_timer
from patent_parsing_tools.patent import Patent


@log
class BagOfWords:
    def __init__(self, dictionary_name):
        """
        >>> bag_of_words.dictionary #doctest: +ELLIPSIS
        {..., 'rp': 4092, 'ru': 4093, 'propanol': 4094, 'shroud': 4095}
        """
        self.dictionary = self._load_dictionary(dictionary_name)
        self.wordcount = WordCount()

    @log_timer
    def parse_all(
        self, patents_directory, destination_directory, package_size
    ):
        patents_list = []
        package_index = 1
        Supervisor._create_directory_if_not_exists(destination_directory)

        for filename in os.listdir(patents_directory):
            patent_filename = os.path.join(patents_directory, filename)
            self.logger.info(
                f"Opening file with serialized patents: {patent_filename}"
            )
            patents_list += self.parse_one_file(patent_filename)
            if len(patents_list) > package_size:
                serialized_patent_filename = os.path.join(
                    destination_directory, f"ml-patents_{package_index}"
                )
                self._serialize_patent_list(
                    serialized_patent_filename, patents_list[:package_size]
                )
                package_index += 1
                patents_list = patents_list[package_size:]
        serialized_patent_filename = os.path.join(
            destination_directory, f"ml-patents_{package_index}"
        )
        self._serialize_patent_list(
            serialized_patent_filename, patents_list[:package_size]
        )

    @log_timer
    def parse_one_file(self, filename):
        """
        >>> serialized_patents = resource_filename("patent_parsing_tools.bow.tests", "xml_tuple_short")
        >>> bag_of_words.parse_one_file(serialized_patents) #doctest: +ELLIPSIS
        [('08923091', [['G', '01', 'V', '1', '36'], ['G', '01', 'S', '7', '28'], ['G', '01', 'S', '7', '292']], {'dual': 2, 'sensor': 120, ...})]
        """
        parsed_patent_list = []
        with open(filename, "rb") as f:
            patent_list = self._load_patent_list(f)
            for patent in patent_list:
                parsed_patent_list.append(self._parse_patent(patent))
        return parsed_patent_list

    def _parse_patent(self, patent):
        """
        >>> patent = Patent()
        >>> patent.title = "ala m4 kota"
        >>> patent.abstract = "ala m4 kota"
        >>> patent.description = "a1a m4 kota"
        >>> patent.claims = "kot m4 alę"
        >>> patent.documentID = "asdf1"
        >>> patent.classification = [['G', '01', 'V', '1', '36']]
        >>> bag_of_words._parse_patent(patent)
        ('asdf1', [['G', '01', 'V', '1', '36']], {'ala': 2, 'm4': 4, 'kota': 3, 'a1a': 1, 'kot': 1, 'al': 1})
        """
        dictionary = self.wordcount.parse_text(patent.title)
        dictionary = self.wordcount.parse_text(patent.abstract, dictionary)
        dictionary = self.wordcount.parse_text(patent.description, dictionary)
        dictionary = self.wordcount.parse_text(patent.claims, dictionary)
        patent.classification
        return patent.documentID, patent.classification, dictionary

    def _serialize_patent_list(self, serialized_patent_filename, patent_list):
        """
        >>> patent_list = [('asdf1', [['G', '01', 'V', '1', '36']], {'ma': 4, 'al': 1, 'ala': 2, 'a1a': 1, 'kot': 1, 'kota': 3})]
        >>> bag_of_words._serialize_patent_list("./final_serialized_patent", patent_list)
        >>> with open("./final_serialized_patent", 'r') as f:
        ...     print(f.read())
        asdf1 [G:01:V:1:36] 444:1 3023:4
        """
        with open(serialized_patent_filename, "w") as f:
            for patent in patent_list:
                patent_as_string = self._patent_to_string(patent)
                f.write(patent_as_string)
        self.logger.info("Serialized data to " + serialized_patent_filename)

    def _patent_to_string(self, patent):
        """
        >>> patent = ('asdf1', [['G', '01', 'V', '1', '36', None]], {'ma': 4, 'al': 1, 'ala': 2, 'a1a': 1, 'kot': 1, 'kota': 3})
        >>> bag_of_words._patent_to_string(patent)
        'asdf1 [G:01:V:1:36:None] 444:1 3023:4'
        """
        classification = " ".join(
            map(":".join, [map(str, x) for x in patent[1]])
        )
        wordcount = {
            self.dictionary[key]: value
            for (key, value) in patent[2].items()
            if key in self.dictionary
        }
        wordcount_as_string = " ".join(
            [f"{x[0]}:{x[1]}" for x in sorted(wordcount.items())]
        )
        return f"{patent[0]} [{classification}] {wordcount_as_string}"

    @staticmethod
    def _load_patent_list(f):
        return pickle.load(f)

    @staticmethod
    def _load_dictionary(dictionary_name):
        dictionary = {}
        index = 0
        with open(dictionary_name, "r") as f:
            for line in f:
                dictionary[line.strip()] = index
                index += 1
        return dictionary


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "python -m patent_parsing_tools.bow.bag_of_words"
            " [directory_with_serialized_patents] [destination_directory]"
            " [dictionary.txt] [package_size > 1024]"
        )
    else:
        patents_directory = sys.argv[1]
        destination_directory = sys.argv[2]
        dictionary_name = sys.argv[3]
        package_size = int(sys.argv[4])

        bag_of_words = BagOfWords(dictionary_name)
        bag_of_words.parse_all(
            patents_directory, destination_directory, package_size
        )
