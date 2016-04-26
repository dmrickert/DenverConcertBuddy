#!/usr/bin/env python

from bs4 import BeautifulSoup # HTML parser
import urllib

class Scrapey:
    def __init__(self):
        self.url = ''
        #self.
        self.webpageData = ''
    def add_url(self, url):
        self.url = url
    def get_webpage(self):
        # Logic to get webpage data
        r = urllib.urlopen(self.url).read()
        soup = BeautifulSoup(r, 'lxml')
        concerts = soup.find_all("li", class_="list-result")
        for concert in concerts:
            title = concert.find(class_="title")
            if title is not None:
                artist = title.getText()
                date = concert.find(class_="time").getText()
                date = date.lstrip('\n')
                date = date.strip(' ')

                print(artist, date)
                #print date


        self.webpageData = 'test'

        print self.webpageData
