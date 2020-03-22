import os
import re
import requests
import sys
from lxml import etree
from patent_parsing_tools.utils.log import log


@log
class Downloader:

    URLS_XPATH = "//a/@href"

    def __init__(self, base_url):
        self.base_url = base_url

    def download_archives(self, directory, begin_year, end_year):
        urls = self.get_urls(begin_year, end_year)
        for url in urls:
            filename = os.path.basename(url)
            self.logger.info(filename)
            local_file = os.path.join(directory, filename)
            if os.path.isfile(local_file):
                self.logger.info("   file already exists")
            else:
                r = requests.get(url, stream=True)
                if r.status_code == 200:
                    with open(local_file, "wb") as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                self.logger.info("   downloaded")

    def get_urls(self, begin_year, end_year):
        content = self.get_base_url_content()
        tree = etree.HTML(content)
        return self.filter_urls(
            tree.xpath(self.URLS_XPATH), begin_year, end_year
        )

    def get_base_url_content(self):
        response = requests.get(self.base_url)
        return response.content

    def filter_urls(self, urls, begin_year, end_year):
        return filter(
            lambda url: self.url_matcher(url, begin_year, end_year), urls
        )

    def url_matcher(self, url, begin_year, end_year):
        match = re.match(r".*\/(?P<year>[0-9]+)\/[a-z0-9_]+\.zip", url)
        if match is None:
            return False
        year = int(match.group("year"))
        return begin_year <= year and year <= end_year


def process_args(argv):
    dir = sys.argv[1]
    if not os.path.isdir(dir):
        os.makedirs(dir)

    try:
        begin_year = int(sys.argv[2])
        end_year = int(sys.argv[3])
    except Exception as e:
        print(e)
        print("incorrect year")

    return dir, begin_year, end_year


if __name__ == "__main__":
    if len(sys.argv) == 4:
        dir, begin_year, end_year = process_args(sys.argv)

        url = (
            "https://www.google.com/googlebooks/uspto-patents-grants-text.html"
        )

        downloader = Downloader(url)
        downloader.download_archives(dir, begin_year, end_year)
    else:
        print("python downloader.py [directory] [year_from] [year_to]")
