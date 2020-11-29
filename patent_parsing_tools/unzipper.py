from zipfile import is_zipfile, ZipFile
from os import listdir, path, unlink
from os.path import join, splitext, basename, isfile
from argparse import Namespace, ArgumentParser

# from patent_parsing_tools import Splitter, log
from patent_parsing_tools.utils.log import log


@log
class Unzipper:
    def __init__(self, directory):
        self.working_directory = directory
        self.temp_dir = join(directory, "temp")
        self.patentDir = "patents"

    def unzip_all(self):
        zip_files = [
            join(self.working_directory, f)
            for f in listdir(self.working_directory)
            if is_zipfile(join(self.working_directory, f))
        ]
        for zip_name in zip_files:
            try:
                zip = ZipFile(zip_name)
                if self.should_be_unzipped(zip):
                    self.logger.info("unzip " + zip_name)
                    zip.extractall(self.temp_dir)
                self.split_patents(
                    self.temp_dir, splitext(basename(zip_name))[0]
                )
                self.clear_temp()
            except Exception as e:
                self.logger.error(e)

    def should_be_unzipped(self, zip):
        if path.exists(
            join(
                self.working_directory,
                self.patentDir,
                splitext(basename(zip.filename))[0],
            )
        ):
            return False
        for file in zip.namelist():
            if not isfile(join(self.working_directory, file)):
                return True
        return False

    def split_patents(self, temp_dir, filename):
        self.logger.info("splitting files")
        xmls = get_files(temp_dir, ".xml")
        splitter = Splitter()

        for file in xmls:
            splitter.split_file(
                file, join(self.working_directory, self.patentDir, filename)
            )

    def clear_temp(self):
        for file in listdir(self.temp_dir):
            file_path = join(self.temp_dir, file)
            try:
                if isfile(file_path):
                    unlink(file_path)
            except Exception as e:
                self.logger.info(e)


def get_files(directory, type):
    return [join(directory, f) for f in listdir(directory) if f.endswith(type)]


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Unzipper")
    parser.add_argument(
        "--directory",
        type=str,
        help="Destination directory where dataset should be downloaded",
        dest="directory",
        required=True,
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    unzipper = Unzipper(args.directory)
    unzipper.unzip_all()


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
