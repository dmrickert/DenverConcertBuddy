#!/usr/bin/env python
import westwood_scrapey

def get_concerts_venue_date(venue, targetDate):
    scraper = westwood_scrapey.Scrapey()
    scraper.set_venue(venue)
    scraper.get_webpage()
    scraper.get_concerts()

    return(scraper.view_concerts_by_date(targetDate))

def get_favorite_venues_all(venues):
    scraper = westwood_scrapey.Scrapey()

    concerts = []

    for venue in venues:
        scraper.set_venue(venue)
        scraper.get_webpage()
        scraper.get_concerts()
        concerts.append(scraper.concerts)

    return concerts

def test_all_functions():
    concertVenues = [
        'Red Rocks Amphitheatre',
        'Fiddler\'s Green Amphitheatre',
        'Fillmore Auditorium',
        'Ogden Theatre',
    ]
    allConcerts = get_favorite_venues_all(concertVenues)

    for venueConcerts in allConcerts:
        print(len(venueConcerts))

    venue = concertVenues[0]
    targetDate = "May 27th"
    targetConcertsByDate = get_concerts_venue_date(venue, targetDate)
    print(len(targetConcertsByDate))

def main( *args ):
    test_all_functions()

if __name__ == '__main__':
    main()
