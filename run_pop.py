__author__ = 'austin'

from pop import crawl_interval
from pop.server_util import server_addr, make_endpoint
from pop.corn import Crawler
import unirest


def found_pop():
    print "Found a popper!"
    unirest.post(server_addr + make_endpoint)


if __name__ == "__main__":
    crawler = Crawler(found_function=found_pop)
    try:
        crawler.crawl()
    except KeyboardInterrupt:
        crawler.stop()
        print "\nBai dood!"




