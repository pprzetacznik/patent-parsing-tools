import sys
import os
from os import listdir
from os.path import join
from random import randint, shuffle
import pickle
from argparse import Namespace, ArgumentParser
from patent_parsing_tools.downloader import Downloader
from patent_parsing_tools.unzipper import Unzipper
from patent_parsing_tools.extractor import Extractor
from patent_parsing_tools.utils.log import log


@log
class Supervisor:
    download_url = (
        "https://www.google.com/googlebooks/uspto-patents-grants-text.html"
    )
    """Docstring for Supervisor class"""

    def __init__(self, working_dir, train_destination, test_destination):
        self.working_dir = working_dir
        self.train_destination = train_destination
        self.test_destination = test_destination
        Supervisor._create_directory_if_not_exists(self.working_dir)
        Supervisor._create_directory_if_not_exists(self.train_destination)
        Supervisor._create_directory_if_not_exists(self.test_destination)

    @staticmethod
    def _create_directory_if_not_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def begin(self, begin_year, end_year):
        self.download_archives(begin_year, end_year)
        self.unzip_patents()
        self.extract_data()

    def download_archives(self, begin_year, end_year):
        self.logger.info("downloading archives")
        downloader = Downloader(self.download_url)
        downloader.download_archives(self.working_dir, begin_year, end_year)

    def unzip_patents(self):
        self.logger.info("unzipping patents")
        unzipper = Unzipper(self.working_dir)
        unzipper.unzip_all()

    def extract_data(self):
        self.logger.info("extracting data")
        extractor = Extractor(self.train_destination)
        patents = get_files(join(self.working_dir, "patents"), ".XML")
        train_patent_list = []
        test_patent_list = []
        num_of_valid_patents = 0
        num_of_invalid_patents = 0
        total_number_of_test_patents = 0

        for patent in patents:
            self.logger.info("extracting " + patent)
            try:
                parsed_patent = extractor.parse(patent)
                if self.is_patent_valid(parsed_patent):
                    num_of_valid_patents += 1
                    if len(test_patent_list) % 1000 == 0:
                        self.logger.info(
                            "train_patent_list has length %d"
                            % (len(train_patent_list))
                        )
                    if randint(1, 10) == 10:  # 10% szansy
                        test_patent_list.append(parsed_patent)
                        total_number_of_test_patents += 1
                    else:
                        train_patent_list.append(parsed_patent)
                else:
                    num_of_invalid_patents += 1
            except Exception as e:
                self.logger.error(f"Message: {e}")
                self.logger.error(
                    f"Number of valid patents was {num_of_valid_patents}, "
                    + f"number of invalid patents was {num_of_invalid_patents}"
                )
                sys.exit()
        self.save_list(test_patent_list, self.test_destination)
        self.save_list(train_patent_list, self.train_destination)
        self.logger.info(
            f"Final number of valid patents was {num_of_valid_patents}, "
            + f"number of invalid patents was {num_of_invalid_patents}"
        )
        self.logger.info(
            f"Total number of test examples is {total_number_of_test_patents}"
        )

    def save_list(self, patent_list, patent_list_destination):
        shuffle(patent_list)
        ind = 0
        patent_list_number = 1
        while ind < len(patent_list):
            with open(
                patent_list_destination
                + os.sep
                + "xml_tuple_"
                + str(patent_list_number),
                "wb",
            ) as f:
                if ind + 1023 > len(patent_list):
                    pickle.dump(
                        patent_list[ind:], f, protocol=pickle.HIGHEST_PROTOCOL
                    )
                else:
                    pickle.dump(
                        patent_list[ind : ind + 1023],
                        f,
                        protocol=pickle.HIGHEST_PROTOCOL,
                    )
            patent_list_number += 1
            ind += 1024
        del patent_list[:]

    def is_patent_valid(self, patent):
        if (
            patent is not None
            and len(patent.classification) > 0
            and patent.abstract is not None
            and patent.title is not None
            and patent.description is not None
            and patent.claims is not None
        ):
            return True
        self.logger.warn("patent " + patent.documentID + " is not valid")
        return False


def get_files(directory, type):
    l = []
    for d in listdir(directory):
        if d.endswith(type):
            l.append(join(directory, d))
        else:
            for f in listdir(join(directory, d)):
                if f.endswith(type):
                    l.append(join(directory, d, f))
    return l


def process_args(argv):
    working_directory = argv[1]
    train_dest = argv[2]
    test_dest = argv[3]

    try:
        begin_year = int(argv[4])
        end_year = int(argv[5])
    except:
        print("incorrect year")

    return working_directory, train_dest, test_dest, begin_year, end_year


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        description=(
            "Download dataset as zip files to the destination directory"
        )
    )
    parser.add_argument(
        "--working-directory",
        type=str,
        help="Working directory",
        dest="working_directory",
        required=True,
    )
    parser.add_argument(
        "--train-destination",
        type=str,
        help="Destination directory where train dataset lands",
        dest="train_destination",
        required=True,
    )
    parser.add_argument(
        "--test-destination",
        type=str,
        help="Destination directory where test dataset lands",
        dest="test_destination",
        required=True,
    )
    parser.add_argument(
        "--year-from",
        type=int,
        help="Year downloading should start from",
        dest="year_from",
        required=True,
    )
    parser.add_argument(
        "--year-to",
        type=int,
        help="Year downloading should end at",
        dest="year_to",
        required=True,
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    supervisor = Supervisor(
        args.working_directory, args.train_destination, args.test_destination
    )
    supervisor.begin(args.year_from, args.year_to)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
