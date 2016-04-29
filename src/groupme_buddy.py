#!/usr/bin/env python3

import groupy
import denver_concert_buddy
import requests
import datetime, sys, fcntl
import os, yaml, string

def get_config_vars(configFileName):
    filePath = os.path.dirname(os.path.realpath(__file__))
    fileName = os.path.join(filePath, configFileName)

    if not os.path.isfile(fileName):
        print('ERROR: No GroupMe configuration file!')
        sys.exit(1)

    with open(fileName, 'r') as f:
        try:
            configVars = yaml.load(f)
        except yaml.YAMLError as exc:
            print(exc)

    return(configVars)

def get_concert_response(text):
    # IMPORTANT: This much match for the date and for the venue
    rstrippers = ' ?!.'

    # To handle any locations with ' on ' we only want the last instance of the split
    date = text.split(' on ')[-1:][0]
    date = date.rstrip(rstrippers) # Get rid of any characters that shouldn't come at the end

    # IMPORTANT: rstrip must match date rstrip or i
    venue = text.lstrip('Leo, who is playing at ').rstrip(rstrippers)
    # Since we did the same rstrip, we know our date variable is on the end
    venue = venue[:-len(date)]
    # The way we handled the split, we know that the next has to be " on "
    venue = venue[:-len(' on ')]
    # Capitalize all words in venue as Westword expects
    venue = venue.title()
    venue = string.capwords(venue, " ")

    # Nobody can ever spell amphitheatre
    if venue == 'Red Rocks':
        venue = 'Red Rocks Amphitheatre'

    try:
        concerts = denver_concert_buddy.get_concerts_venue_date(venue, date)
    except Exception:
        # If something goes wrong we want the others to still work
        print(text, date, venue)
        return False

    # No concert was found...
    if len(concerts) == 0:
        return 'I don\'t think anyone is at ' + venue + ' on ' + date

    # Could be multiple artists!
    artists = ''
    for concert in concerts:
        if artists:
            artists = artists + " & " + concert['artist']
        else:
            artists = artists + concert['artist']

    # Format the response to send
    response = artists + ' is playing at ' + concerts[0]['location'] + ' on ' + concerts[0]['date']

    return response

def analyze_text( text ):
    # Do the language processing.  Strict formatting is a disappointment...
    response = False
    if text.startswith('Leo,'):
        # Find the artist/time given a venue/date
        if text.startswith('Leo, who is playing at '):
            response = get_concert_response(text)
        # Let the person know that he wanted to respond if he knew how...
        else:
            response = 'I don\'t know what you are asking'

    return response

def get_groupme_messages( groupmeName, timeDelay ):
    # Only want messages between now and the time delay specified in seconds
    # Ex. if timedelay is 30, it'll grab messages from the last 30 seconds
    timePeriod = datetime.datetime.now() - datetime.timedelta(seconds=timeDelay)

    # Pull all of our groups and then find the one we want
    groups = groupy.Group.list()
    group = groups.filter(name__contains=groupmeName).first

    messages = group.messages()
    targMessages = messages.filter(created_at__gt=timePeriod)
    targMessages.reverse()

    # Ignore the other data from the messages for now...
    # Might be nice to not though so we can keep track of who's who
    messageArray = []
    for message in targMessages:
        messageArray.append(message.text)

    return messageArray

def message_groupme( message, botId ):
    groupmeBotsUrl = 'https://api.groupme.com/v3/bots/post'
    # To post as a bot you send a POST to a specific URL formatted as such
    r = requests.post(groupmeBotsUrl, data={"text":message, "bot_id":botId})

def main( *args ):
    # Pull our variables from a YAML config file
    groupmeConfig = get_config_vars( 'groupme.cfg' )

    # Specify the API_KEY... Not sure this is the best way to do it but it seems to work
    groupy.config.API_KEY = groupmeConfig['GroupMeKey']

    # Pull our groupme messages from the last 60 seconds
    messages = get_groupme_messages( groupmeConfig['GroupName'], 60)

    # Loop through each groupme message and see if there's a command for the bot
    for message in messages:
        response = analyze_text(message)
        # Response is False if it's a message not for Leo
        if response:
            print(message, response)
            message_groupme(response, groupmeConfig['BotId'])

if __name__ == '__main__':
    main()
