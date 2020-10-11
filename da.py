#!/usr/bin/env python3

import sys
from urllib.request import urlopen, Request
from html.parser import HTMLParser

def linux_distro():
    with open("/etc/os-release") as f:
        d = {}
        for line in f:
            k,v = line.rstrip().split("=")
            d[k] = v
    return d['ID']
    

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.dist = linux_distro()
        self.div_finded = False
        self.dd_finded = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if ('class', f'command-install intall-{self.dist}') in attrs:
                self.div_finded = True
        if self.div_finded and tag == 'dd':
            self.dd_finded = True

    def handle_data(self, data):
        if self.dd_finded:
            if data.strip():
                print(f'{self.dist.capitalize()} : {data}')
            
    def handle_endtag(self, tag):
        if tag == 'dd' and self.dd_finded:
            self.div_finded = False
            self.dd_finded = False


if __name__ == "__main__":
    parser = MyHTMLParser()
    if len(sys.argv) < 2:
        exit(1)
    url = f'https://command-not-found.com/{sys.argv[1]}'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(req).read().decode("utf-8")
    parser.feed(data)