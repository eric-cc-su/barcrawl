# CS4800 - Mini Pacman Bar Hopping
# Input:   Cities to visit
# Output:  Route to the highest rated bar in each city

import json, requests # for making request to Google Maps
import urllib2, sys, time
import yelp
import tsp_solver

#Get the coordinates of the origin
def get_origin(oAddress):
    url='https://maps.googleapis.com/maps/api/geocode/json'
    params = dict(address=oAddress)

    # Send request to Google Maps
    resp = requests.get(url=url, params=params)
    data = resp.json()
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    return('{},{}'.format(str(lat),str(lng)))

# ------
# STEP 1 - Get top restaurants
# ------

# coordinates of locations
locations = []
# User-friendly Addresses
prettyLocations = []

# Get origin address
origin = get_input('Enter starting address (Ex: \'300 Huntington Avenue, Boston\'):  ')
originCoordinates = get_origin(origin)
locations.append(originCoordinates)
prettyLocations.append(origin)
# Get cities
cities = get_input('Enter cities (Ex: \'Boston,Cambridge\'):  ').split(',')

print('-' * 50)
print('Getting bars...')
# Get list of top restaurants in each city
for city in cities:
   try:
       print('')
       response = yelp.query_api('bars', city)
       #pprint.pprint(response)
       locations.append(str(response.get('location').get('coordinate').get('latitude')) + ',' +
                        str(response.get('location').get('coordinate').get('longitude')))
       # change to use coordinates to be more accurate
       # Print out restaurant name and address
       prettyName = ""
       print(city + ':')
       print(response.get('name') + ": " + str(response.get('rating')))
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
distances_matrix = [[0]*len(locations) for x in xrange(len(locations))]
pairings = {}

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
           time.sleep(0.5)
           resp = requests.get(url=url, params=params)
           data = json.loads(resp.text)

           # Storing distances in matrix for tsp_solver
           distances_matrix[i][j] = data.get('routes')[0].get('legs')[0].get('distance').get('value')
           distances_matrix[j][i] = data.get('routes')[0].get('legs')[0].get('distance').get('value')

           #stores A-to-B duration (seconds) and distance (meters) data
           pairings['{}-{}'.format(i,j)] = {
           "distance": data.get('routes')[0].get('legs')[0].get('distance').get('value'),
           "duration": data.get('routes')[0].get('legs')[0].get('duration').get('value')
           }
           print('\nFROM: ' + prettyLocations[i] + "\nTO: "+ prettyLocations[j] + '\nDistance: ' + data.get('routes')[0].get('legs')[0].get('distance').get('text'))
           print('Time: ' + data.get('routes')[0].get('legs')[0].get('duration').get('text'))

print('-' * 50)
# ------
# STEP 3 - Algorithm to find shortest path
# ------
print('Calculating shortest route...')
cities_index = solve_tsp(distances_matrix, 3)

for city in cities_index:
    print(prettyLocations[city])
