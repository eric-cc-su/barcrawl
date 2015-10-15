# CS4800 - Mini Pacman Bar Hopping
# Input:   Cities to visit
# Output:  Route to the highest rated bar in each city

import json, requests # for making request to Google Maps
import urllib2, sys, time
import yelp
import tsp_solver

#SEARCH_LIMIT = 1

#Get the coordinates of the origin
def get_origin(oAddress):
    url='https://maps.googleapis.com/maps/api/geocode/json'
    params = dict(address=oAddress)

    # Send request to Google Maps
    resp = requests.get(url=url, params=params)
    data = resp.json()
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    address_components = data['results'][0]['address_components']
    for item in address_components:
        if "locality" in item["types"]:
            city = item["long_name"]
    try:
        returnDict = {"coordinates": '{},{}'.format(str(lat),str(lng)), "city": city}
    except:
        return False
    return(returnDict)

# ------
# STEP 1 - Get top restaurants
# ------
def main(cities, origin_address, origin_coordinates, search_limit=1):
    SEARCH_LIMIT = 1
    if search_limit != 1:
        SEARCH_LIMIT = search_limit
    # coordinates of locations
    locations = []
    # User-friendly Addresses
    prettyLocations = []

    locations.append(origin_coordinates)
    prettyLocations.append(['Origin',origin_address])

    counter = 0
    # Get list of top restaurants in each city
    for city in cities:
       try:
           response = yelp.query_api('bars', city, SEARCH_LIMIT)
           for item in response:
               locations.append(str(item.get('location').get('coordinate').get('latitude')) + ',' +
                                str(item.get('location').get('coordinate').get('longitude')))
               # change to use coordinates to be more accurate
               # Print out restaurant name and address
               prettyName = ""
               if len(item.get('location').get('display_address')) > 0:
                   prettyName += item.get('location').get('display_address')[0]
                   #print(item.get('location').get('display_address')[0])
               if len(item.get('location').get('display_address')) > 1:
                   prettyName += ", "+item.get('location').get('display_address')[1]
                   #print(item.get('location').get('display_address')[1])
               if len(item.get('location').get('display_address')) > 2:
                   prettyName += ", "+item.get('location').get('display_address')[2]
                   #print(item.get('location').get('display_address')[2])
               prettyLocations.append([item.get('name'),prettyName])
       except urllib2.HTTPError as error:
           sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

    # ------
    # STEP 2 - Get distances between each restaurant
    # ------
    # Generate list of locations to visit in order
    url = 'http://maps.googleapis.com/maps/api/directions/json'

    # Create 2D array to keep track of pairs of locations - USE NUMPY LATER
    pairs = [[0]*len(locations) for x in xrange(len(locations))]
    distances_matrix = [[0]*len(locations) for x in xrange(len(locations))]

    # Numbers to indicate progress
    lookupNum = 0
    for i in range(len(locations) - 1):
        lookupNum += (i+1)
    counter = 0

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
               counter += 1
               sys.stdout.write("\rGetting Distances...%d%%" % int((float(counter)/lookupNum) * 100))
               sys.stdout.flush()

    # ------
    # STEP 3 - Algorithm to find shortest path
    # ------
    # Returns route cycle

    print(distances_matrix)
    cities_index = tsp_solver.solve_tsp(distances_matrix, 3)

    # Start and end cycle at start location
    #print('\nRoute:')
    route_distance = 0
    previous = 0
    for index, city in enumerate(cities_index):
        route_distance += distances_matrix[previous][city]
        previous = city
    route_distance += distances_matrix[cities_index[-1]][0]

    print('\nDone!')
    route_dict = {"origin_coordinates":{"lat": float(origin_coordinates.split(",")[0]),
                                        "lng": float(origin_coordinates.split(",")[1])},
                  "route_coordinates":[],
                  "route_names":[],
                  "route_addresses":[]}
    for item in cities_index:
        coordinates = locations[item].split(",")
        coordict = {"lat": float(coordinates[0]),
                    "lng": float(coordinates[1])}
        route_dict["route_coordinates"].append(coordict)
        route_dict["route_names"].append(prettyLocations[item][0])
        route_dict["route_addresses"].append(prettyLocations[item][1])

    return route_dict
