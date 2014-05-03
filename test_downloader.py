from unittest import TestCase
from downloader import Downloader

class TestDownloader(TestCase):
    def test_url_matcher_matches_url_from_given_period(self):
        downloader = Downloader('')
        url = 'http://somedomain/2012/patent.zip'
        matched = downloader.url_matcher(url, 2012, 2013)
        assert matched

    def test_url_matcher_doesnt_match_url_out_of_given_period(self):
        downloader = Downloader('')
        url = 'http://somedomain/2011/patent.zip'
        matched = downloader.url_matcher(url, 2012, 2013)
        assert not matched

    def test_url_matcher_matches_only_zip_files(self):
        downloader = Downloader('')
        url = 'http://somedomain/2012/patent.tgz'
        matched = downloader.url_matcher(url, 2012, 2013)
        assert matched