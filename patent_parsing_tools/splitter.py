import os
import re
import sys
from patent_parsing_tools.utils.log import log


@log
class Splitter:
    PATENT_TAG = "us-patent-grant"

    def __init__(self):
        self.num_ignored = 0

    def get_headers_and_filename(self, file):
        headers = []
        for i in range(3):
            line = file.readline()
            headers.append(line)

        if not headers[2].startswith("<%s" % self.PATENT_TAG):
            self.logger.info(
                str(self.num_ignored)
                + ". ignoring "
                + headers[2][1 : headers[2].index(" ")]
            )
            self.num_ignored += 1
            return None, None

        node = re.match(r".*file=.([^ ]*)\".*", headers[2])
        if node is None:
            self.logger.warning("file attribute not found")
            raise Exception("file attribute not found")
        return headers, node.group(1)

    def ingore_file(self, fread):
        while True:
            line = fread.readline()
            if line.startswith("</%s" % self.PATENT_TAG):
                break

    def save_file(self, dir, filename, fread, headers):
        fwrite = open(os.path.join(dir, filename), "w")
        for line in headers:
            fwrite.write(line)
        while True:
            line = fread.readline()
            fwrite.write(line)
            if line.startswith("</%s" % self.PATENT_TAG):
                break

    def split_file(self, input_file, dir):
        if os.path.exists(dir):
            self.logger.info("Skipping directory " + dir)
            return

        fread = open(input_file)

        if not os.path.isdir(dir):
            os.makedirs(dir)

        eof = os.fstat(fread.fileno()).st_size
        while fread.tell() < eof:
            headers, filename = self.get_headers_and_filename(fread)
            if filename is None:
                self.ingore_file(fread)
                continue
            self.logger.info("Saving splitted file %s" % (filename))
            self.save_file(dir, filename, fread, headers)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        input = sys.argv[1]
        dir = sys.argv[2]
        if os.path.isfile(input):
            splitter = Splitter()
            splitter.split_file(input, dir)
        else:
            print(f"File: {input} doesn't exist")
    else:
        print("python splitter.py [input] [output_dir]")
