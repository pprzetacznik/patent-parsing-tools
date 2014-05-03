# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import re
import urllib
import urllib2
from lxml import etree

class Downloader():
    URLS_XPATH='//a/@href'

    def __init__(self, base_url):
        self.base_url = base_url

    def download_archives(self, directory, begin_year, end_year):
        urls = self.get_urls(begin_year, end_year)
        for url in urls:
            print "Downloading", url, "..."
            filename = os.path.basename(url)
            urllib.urlretrieve(url, os.path.join(directory, filename))
            print "OK"

    def get_urls(self, begin_year, end_year):
        content = self.get_base_url_content()
        tree = etree.HTML(content)
        return self.filter_urls(tree.xpath(self.URLS_XPATH), begin_year, end_year)

    def get_base_url_content(self):
        response = urllib2.urlopen(self.base_url)
        return response.read()

    def filter_urls(self, urls, begin_year, end_year):
        url_filter = lambda url: self.url_matcher(url, begin_year, end_year)
        return filter(url_filter, urls)

    def url_matcher(self, url, begin_year, end_year):
        match = re.match(r".*\/(?P<year>[0-9]+)\/[a-z0-9_]+\.zip", url)
        if match is None:
            return False
        year = int(match.group('year'))
        return begin_year <= year and year <= end_year

downloader = Downloader('https://www.google.com/googlebooks/uspto-patents-grants-text.html')
downloader.download_archives('C:\\tmp', 2002, 2014)