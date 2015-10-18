# Barcrawl

CS4800 Algorithms final project to provide an optimal bar crawl path from city to city. The objective is to implement a Traveling Salesman Problem approximation algorithm.

This project has now been developed as a Django web application and deployed to [www.gobarcrawl.com](http://www.gobarcrawl.com/).

![Barcrawl web app](barcrawl.gif)

## Technologies
- Python 2
- Google Maps Directions API
- Google Maps Geocode API
- Google Maps Javascript API
- Yelp Business API
- Yelp Search API

## Using the Web Application
1. The user inputs their origin address
2. The user inputs other cities to visit (optional)
3. If the user does not input other cities to visit, the user inputs the number
of bars in their origin city to visit
4. Work is done by the Python program in the back-end
5. User is given a map and an ordered list of bars to visit

## Running the Python Program
In terminal/command console:
`python barcrawl.py`

## Process - Python Application
1. The user inputs the origin city
2. The origin city coordinates are looked up via Google Geocode API and saved in a list (AKA `locations`)
3. The user inputs a list of cities to visit (AKA `cities`)
4. For every city in `cities` the Yelp API is called to find the top bar in each city
5. Pairs are generated in numerical order and Google Directions API is used to find the distance and route duration between cities. Direction is not taken into account, therefore 0 -> 1 and 1 -> 0 will only be queried once.
6. Each pair is saved in a dictionary (AKA `pairings`) in the format:

    `{'0-1': {'distance': int (meters), 'duration': int (seconds)}}`

7. Optimal path algorithm is implemented

## Data Structures
### locations
This is the list of location coordinates. Each coordinate is a string.

    locations = [
      'latitude,longitude',
      'latitude,longitude',...
    ]
### prettyLocations
This is the list of user-friendly locations. Each item is a string.

    prettyLocations = [
      'Bar Name, Street Address, City, ZIP',
      'Bar Name, Street Address, City, ZIP',...
    ]

## Sample Yelp response

    {u'categories': [[u'Dive Bars', u'divebars']],
    u'display_phone': u'+1-617-654-9944',
    u'id': u'biddy-earlys-boston',
    u'image_url': u'http://s3-media2.fl.yelpcdn.com/bphoto/MAI85AyMSV41pGDIRFsHtA/ms.jpg',
    u'is_claimed': True,
    u'is_closed': False,
    u'location': {u'address': [u'141 Pearl St'],
                 u'city': u'Boston',
                 u'coordinate': {u'latitude': 42.3546486,
                                 u'longitude': -71.0537415},
                 u'country_code': u'US',
                 u'cross_streets': u'High St & Purchase St',
                 u'display_address': [u'141 Pearl St',
                                      u'Financial District',
                                      u'Boston, MA 02110'],
                 u'geo_accuracy': 8.0,
                 u'neighborhoods': [u'Financial District'],
                 u'postal_code': u'02110',
                 u'state_code': u'MA'},
    u'mobile_url': u'http://m.yelp.com/biz/biddy-earlys-boston',
    u'name': u"Biddy Early's",
    u'phone': u'6176549944',
    u'rating': 4.5,
    u'rating_img_url': u'http://s3-media2.fl.yelpcdn.com/assets/2/www/img/99493c12711e/ico/stars/v1/stars_4_half.png',
    u'rating_img_url_large': u'http://s3-media4.fl.yelpcdn.com/assets/2/www/img/9f83790ff7f6/ico/stars/v1/stars_large_4_half.png',
    u'rating_img_url_small': u'http://s3-media2.fl.yelpcdn.com/assets/2/www/img/a5221e66bc70/ico/stars/v1/stars_small_4_half.png',
    u'review_count': 162,
    u'reviews': [{u'excerpt': u"You honestly can't go wrong with $2 PBRs and $6 shots. I can't say I remember much of my experience here, but goddamn did they have amazing onion rings. The...",
                 u'id': u'YzznYPDMofGOuLcnNlY1uQ',
                 u'rating': 5,
                 u'rating_image_large_url': u'http://s3-media3.fl.yelpcdn.com/assets/2/www/img/22affc4e6c38/ico/stars/v1/stars_large_5.png',
                 u'rating_image_small_url': u'http://s3-media1.fl.yelpcdn.com/assets/2/www/img/c7623205d5cd/ico/stars/v1/stars_small_5.png',
                 u'rating_image_url': u'http://s3-media1.fl.yelpcdn.com/assets/2/www/img/f1def11e4e79/ico/stars/v1/stars_5.png',
                 u'time_created': 1438553780,
                 u'user': {u'id': u'NIXvVPlvmxorOgZLa0U_hA',
                           u'image_url': u'http://s3-media2.fl.yelpcdn.com/photo/8WDU8alAx7gPz0k7VZV--Q/ms.jpg',
                           u'name': u'Shani T.'}}],
    u'snippet_image_url': u'http://s3-media2.fl.yelpcdn.com/photo/8WDU8alAx7gPz0k7VZV--Q/ms.jpg',
    u'snippet_text': u"You honestly can't go wrong with $2 PBRs and $6 shots. I can't say I remember much of my experience here, but goddamn did they have amazing onion rings. The...",
    u'url': u'http://www.yelp.com/biz/biddy-earlys-boston'}

## Sample Bar Crawl Response

    Enter starting address (Ex: 300 Huntington Avenue, Boston):  300 Huntington Ave, Boston
    Enter cities (Ex: Boston,Cambridge,LA,Philadelphia):  Boston,Cambridge,Philadelphia
    --------------------------------------------------
    Getting bars...

    Querying http://api.yelp.com/v2/search/? ...
    Querying business info for the top result "biddy-earlys-boston" ...
    Querying http://api.yelp.com/v2/business/biddy-earlys-boston? ...
    Result for business "biddy-earlys-boston" found:
    Boston:
    Biddy Early's
    141 Pearl St
    Financial District
    Boston, MA 02110

    Querying http://api.yelp.com/v2/search/? ...
    Querying business info for the top result "the-druid-cambridge" ...
    Querying http://api.yelp.com/v2/business/the-druid-cambridge? ...
    Result for business "the-druid-cambridge" found:
    Cambridge:
    The Druid
    1357 Cambridge St
    Inman Square
    Cambridge, MA 02139

    Querying http://api.yelp.com/v2/search/? ...
    Querying business info for the top result "franky-bradleys-philadelphia" ...
    Querying http://api.yelp.com/v2/business/franky-bradleys-philadelphia? ...
    Result for business "franky-bradleys-philadelphia" found:
    Philadelphia:
    Franky Bradley's
    1320 Chancellor St
    Washington Square West
    Philadelphia, PA 19107
    --------------------------------------------------
    Getting distances...

    FROM: 300 Huntington Ave, Boston
    TO: 141 Pearl St, Financial District, Boston, MA 02110
    Distance: 2.2 mi
    Time: 16 mins

    FROM: 300 Huntington Ave, Boston
    TO: 1357 Cambridge St, Inman Square, Cambridge, MA 02139
    Distance: 2.7 mi
    Time: 17 mins

    FROM: 300 Huntington Ave, Boston
    TO: 1320 Chancellor St, Washington Square West, Philadelphia, PA 19107
    Distance: 308 mi
    Time: 5 hours 12 mins

    FROM: 141 Pearl St, Financial District, Boston, MA 02110
    TO: 1357 Cambridge St, Inman Square, Cambridge, MA 02139
    Distance: 4.4 mi
    Time: 15 mins

    FROM: 141 Pearl St, Financial District, Boston, MA 02110
    TO: 1320 Chancellor St, Washington Square West, Philadelphia, PA 19107
    Distance: 309 mi
    Time: 5 hours 11 mins

    FROM: 1357 Cambridge St, Inman Square, Cambridge, MA 02139
    TO: 1320 Chancellor St, Washington Square West, Philadelphia, PA 19107
    Distance: 307 mi
    Time: 5 hours 13 mins
    --------------------------------------------------
    Calculating shortest route...
    Optimizing solution...

    Route:
    0 miles driven - origin
    300 Huntington Ave, Boston

    2 miles driven - The Druid
    1357 Cambridge St, Inman Square, Cambridge, MA 02139

    309 miles driven - Franky Bradley's
    1320 Chancellor St, Washington Square West, Philadelphia, PA 19107

    619 miles driven - Biddy Early's
    141 Pearl St, Financial District, Boston, MA 02110

    621 miles driven - origin
    300 Huntington Ave, Boston

    Total Distance Travelled: 621 miles

    Done!
