#!/usr/bin/env python

from bs4 import BeautifulSoup # HTML parser
import urllib.parse, urllib.request
import sys
from dateutil import parser as dateparser

class Scrapey:
    def __init__(self):
        self.baseUrl = 'http://www.westword.com/concerts?sort=date&direction=asc&venues[]='
        self.url = ''
        self.webpageData = ''
        self.concerts = ''

    def set_venue(self, venue):
        self.url = self.baseUrl + urllib.parse.quote(venue)

    def get_webpage(self):
        # Logic to get webpage data
        self.webpageData = urllib.request.urlopen(self.url).read()

    def get_concerts(self):
        soup = BeautifulSoup(self.webpageData, "html5lib")
        concerts = soup.find_all("li", class_="list-result")

        # Would be better to put this in a database instead of a list of dictionaries
        concertsArray = []
        for concert in concerts:
            title = concert.find(class_="title")
            if title is not None:
                concertDict = {}
                concertDict['artist'] = title.getText()
                concertDict['date'] = concert.find(class_="time").getText().strip('\n').strip(' ')
                concertDict['conformDate'] = dateparser.parse(concertDict['date']).strftime('%m-%d')

                concertDict['cost'] = concert.find(class_='price').getText()
                concertDict['location'] = concert.find(class_='location').getText().strip('\n').strip(' ').strip('\n')

                concertsArray.append(concertDict)

        self.concerts = concertsArray
        return

    def view_concerts_by_date(self, targetDate):
        conformedTargetDate = dateparser.parse(targetDate).strftime('%m-%d')

        concertsByDate = []

        # Looping through each dictionary in a dictionary list is not very fast..
        for concert in self.concerts:
            if concert['conformDate'] == conformedTargetDate:
                concertsByDate.append(concert)

        return concertsByDate
