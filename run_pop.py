"""
    Will crawl some social places and look for making pop triggers
"""
__author__ = 'austin'

from pop.server_util import server_addr, make_ext
from pop.corn import Crawler
import unirest
from urlparse import urljoin
from urllib import urlencode


def found_pop(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """

    url = urljoin(server_addr, make_ext)
    if 'commands' in kwargs:
        url = urljoin(url, "?" + urlencode(kwargs['commands']))
    print unirest.post(url)


if __name__ == "__main__":
    crawler = Crawler(found_function=found_pop)
    try:
        crawler.crawl()
    except KeyboardInterrupt:
        crawler.stop()
        print "\nBai dood!"




