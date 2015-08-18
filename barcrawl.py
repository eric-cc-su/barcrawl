# CS4800 - Mini Pacman Bar Hopping
# Input:   Cities to visit
# Output:  Route to the highest rated restaurant in each city

#import numpy as np # setup later
import json, requests # for making request to Google Maps

# YELP API -- Need to separate into module later --
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'bars'
DEFAULT_LOCATION = 'Boston, MA'
SEARCH_LIMIT = 1
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'MapfPwZlG1iuz9Acja1hUA'
CONSUMER_SECRET = 'ab5uLcItYvNO4FraBskwug5FKoc'
TOKEN = 'dli5QisyRwIiG05K4R34VRO3HhpUEYeU'
TOKEN_SECRET = 'Z949X5mUkHw_eSTQA_nxFft0UJ4'

def request(host, path, url_params=None):
   """Prepares OAuth authentication and sends the request to the API.
   Args:
       host (str): The domain host of the API.
       path (str): The path of the API after the domain.
       url_params (dict): An optional set of query parameters in the request.
   Returns:
       dict: The JSON response from the request.
   Raises:
       urllib2.HTTPError: An error occurs from the HTTP request.
   """
   url_params = url_params or {}
   url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

   consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
   oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

   oauth_request.update(
       {
           'oauth_nonce': oauth2.generate_nonce(),
           'oauth_timestamp': oauth2.generate_timestamp(),
           'oauth_token': TOKEN,
           'oauth_consumer_key': CONSUMER_KEY
       }
   )
   token = oauth2.Token(TOKEN, TOKEN_SECRET)
   oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
   signed_url = oauth_request.to_url()

   print u'Querying {0} ...'.format(url)

   conn = urllib2.urlopen(signed_url, None)
   try:
       response = json.loads(conn.read())
   finally:
       conn.close()

   return response

def search(term, location):
   """Query the Search API by a search term and location.
   Args:
       term (str): The search term passed to the API.
       location (str): The search location passed to the API.
   Returns:
       dict: The JSON response from the request.
   """

   url_params = {
       'term': term.replace(' ', '+'),
       'location': location.replace(' ', '+'),
       'limit': SEARCH_LIMIT
   }
   return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
   """Query the Business API by a business ID.
   Args:
       business_id (str): The ID of the business to query.
   Returns:
       dict: The JSON response from the request.
   """
   business_path = BUSINESS_PATH + business_id

   return request(API_HOST, business_path)

def query_api(term, location):
   """Queries the API by the input values from the user.
   Args:
       term (str): The search term to query.
       location (str): The location of the business to query.
   """
   response = search(term, location)

   businesses = response.get('businesses')

   if not businesses:
       print u'No businesses for {0} in {1} found.'.format(term, location)
       return

   business_id = businesses[0]['id']

   # Print out info for top place
   # print u'{0} businesses found, querying business info for the top result "{1}" ...'.format(
   #     len(businesses),
   #     business_id
   # )

   response = get_business(business_id)

   #print u'Result for business "{0}" found:'.format(business_id)
   # pprint.pprint(response, indent=2)
   return response

# def main():
#     parser = argparse.ArgumentParser()
#
#     # Arguments (key term & location)
#     parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
#     parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')
#
#     input_values = parser.parse_args()
#
#     # Make request w/ arguments
#     try:
#         query_api(input_values.term, input_values.location)
#     except urllib2.HTTPError as error:
#         sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

# -- END OF YELP

# ------
# STEP 1 - Get top restaurants
# ------

# Addresses (origin and restaurants)
locations = []
# Printable Addresses
prettyLocations = []
# Get starting address
origin = input('Enter starting address (Ex: \'300 Huntington Avenue, Boston\'):  ')
locations.append(origin)
prettyLocations.append(origin)
# Get cities
cities = input('Enter cities (Ex: \'Boston,Cambridge\'):  ').split(',')

print('-' * 50)
print('Getting restaurants...')
# Get list of top restaurants in each city
for city in cities:
   try:
       print('')
       response = query_api(DEFAULT_TERM, city)
       #pprint.pprint(response.get('location'))
       locations.append(str(response.get('location').get('coordinate').get('latitude')) + ',' +
                        str(response.get('location').get('coordinate').get('longitude')))
       # change to use coordinates to be more accurate
       # Print out restaurant name and address
       prettyName = ""
       print(city + ':')
       print(response.get('name'))
       if len(response.get('location').get('display_address')) > 0:
           prettyName += response.get('location').get('display_address')[0]
           print(response.get('location').get('display_address')[0])
       if len(response.get('location').get('display_address')) > 1:
           prettyName += ", "+response.get('location').get('display_address')[1]
           print(response.get('location').get('display_address')[1])
       if len(response.get('location').get('display_address')) > 2:
           prettyName += ", "+response.get('location').get('display_address')[2]
           print(response.get('location').get('display_address')[2])
       prettyLocations.append(prettyName)
   except urllib2.HTTPError as error:
       sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

print('-' * 50)

# ------
# STEP 2 - Get distances between each restaurant
# ------
print('Getting distances...')
# Generate list of locations to visit in order
url = 'http://maps.googleapis.com/maps/api/directions/json'

# NEED TO FIX - need to skip over duplicate i,j pairs to reduce requests
# Create 2D array to keep track of pairs of locations - USE NUMPY LATER
pairs = [[0]*len(locations) for x in xrange(len(locations))]

for i in range(0, len(locations)):
   for j in range(0, len(locations)):
       # Skip over duplicate pairs of locations to reduce requests
       if pairs[i][j] != 1 and i != j:
           # Set parameters
           params = dict(
               origin=locations[i],
               destination=locations[j]
           )

           # Set to 1 to skip later
           pairs[i][j] = 1
           pairs[j][i] = 1

           # Send request to Google Maps
           resp = requests.get(url=url, params=params)
           data = json.loads(resp.text)
           #pprint.pprint(data)
           print('\nFROM: ' + prettyLocations[i] + "\nTO: "+ prettyLocations[j] + '\nDistance: ' +
                 data.get('routes')[0].get('legs')[0].get('distance').get('text'))
           print('Time: ' +
                 data.get('routes')[0].get('legs')[0].get('duration').get('text'))

print('-' * 50)
# ------
# STEP 3 - Algorithm to find shortest path
# ------
print('Calculating shortest route...')
