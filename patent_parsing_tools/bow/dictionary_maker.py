import os
import sys
import pickle
import operator
from argparse import Namespace, ArgumentParser
from patent_parsing_tools.bow.wordcount import WordCount
from patent_parsing_tools.utils.log import log, log_timer


@log
class DictionaryMaker:
    """
    >>> dictionary_maker = DictionaryMaker()
    >>> print(dictionary_maker) #doctest: +ELLIPSIS
    <patent_parsing_tools.bow.dictionary_maker.DictionaryMaker object ...
    """

    def __init__(self):
        self.wordcount = WordCount()
        self.wordcount_dictionary = {}

    @log_timer
    def parse(self, directory, max_parsed_patents):
        n = 0
        for fn in os.listdir(directory):
            self.logger.info(directory + os.sep + fn)
            patent_list = pickle.load(open(directory + os.sep + fn, "rb"))

            for patent in patent_list:
                self.wordcount.parse_text(
                    patent.abstract, self.wordcount_dictionary
                )
                self.wordcount.parse_text(
                    patent.description, self.wordcount_dictionary
                )
                self.wordcount.parse_text(
                    patent.claims, self.wordcount_dictionary
                )
                self.wordcount.parse_text(
                    patent.title, self.wordcount_dictionary
                )
                n += 1
                if n > max_parsed_patents:
                    break
        self.logger.info(f"Parsed: {str(n)} patents")

    @log_timer
    def dump(self, dictionary_name, dict_max_size):
        sorted_wordcount = sorted(
            self.wordcount_dictionary.items(),
            key=operator.itemgetter(1),
            reverse=True,
        )[:dict_max_size]
        with open(dictionary_name, "w") as f:
            keys = [item[0] for item in sorted_wordcount]
            f.write("\n".join(keys))


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        description=(
            "Download dataset as zip files to the destination directory"
        )
    )
    parser.add_argument(
        "--train-directory",
        type=str,
        help="Train directory",
        dest="train_directory",
        required=True,
    )
    parser.add_argument(
        "--max-patents",
        type=int,
        help="Maximum numer of parsed patents",
        dest="max_parsed_patents",
        required=True,
    )
    parser.add_argument(
        "--dictionary",
        type=str,
        help="Path to dictionary text file",
        dest="dictionary",
        required=True,
    )
    parser.add_argument(
        "--dict-max-size",
        type=int,
        help="Maximum size of dictionary",
        dest="dict_max_size",
        required=True,
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    dictionary_maker = DictionaryMaker()
    dictionary_maker.parse(args.train_directory, args.max_parsed_patents)
    dictionary_maker.dump(args.dictionary_name, args.dict_max_size)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
