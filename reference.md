##Sample Yelp response

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

##Proposed Bar Ranking
Based on:
- distance
- rating
- review_count
