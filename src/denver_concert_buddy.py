#!/usr/bin/env python
import googley_calendar
import westwood_scrapey

def main( *args ):
    # Get Red Rocks Events
    redRocks = westwood_scrapey.Scrapey()
    redRocks.add_url('http://www.westword.com/concerts?sort=date&direction=asc&venues[]=Red%20Rocks%20Amphitheatre')
    redRocks.get_webpage()

if __name__ == '__main__':
    main()
