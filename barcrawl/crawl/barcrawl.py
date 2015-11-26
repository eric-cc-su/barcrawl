# CS4800 - Mini Pacman Bar Hopping
# Input:   Cities to visit
# Output:  Route to the highest rated bar in each city

import datetime
import json, requests # for making request to Google Maps
import os
import urllib2, sys, time
import yelp
import tsp_solver

from crawl.models import City, Bar, Distance


#SEARCH_LIMIT = 1

def get_server_key():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gserverFile = open(os.path.join(BASE_DIR, "googleServer.txt"))
    key = gserverFile.readline().strip()
    gserverFile.close()
    return key

#Get the coordinates of the origin
def get_origin(oAddress):
    url='https://maps.googleapis.com/maps/api/geocode/json'
    params = dict(address = oAddress,
                  key = get_server_key())
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
        originCity = City.objects.get(city=city.lower())

        # Calculate last update of city info
        datedelta = (datetime.date.today() - originCity.date).days

        # City exists in database and is up to date
        # and is associated with enough bars
        if originCity and datedelta < 31 \
                and Bar.objects.filter(city=originCity).count() >= search_limit:

            # SELECT * FROM crawl_bar
            # WHERE city_id = originCity
            # ORDER BY order ASC
            # LIMIT search_limit
            bars = Bar.objects.filter(city=originCity).order_by('priority')[:search_limit]

            for item in bars:
                locations.append(str(item.lat)+','+str(item.lng))
                prettyLocations.append([item.name,item.address])

        else:
            try:
                response = yelp.query_api('bars', city, SEARCH_LIMIT)

                for index, item in response:
                    locationInfo = item.get('location')
                    locationCoordinates = locationInfo.get('coordinate')
                    displayAddress = locationInfo.get('display_address')

                    # City does not exist in database
                    if not originCity:
                        cityString = locationInfo.get('city').lower()
                        stateString = locationInfo.get('state_code')
                        countryString = locationInfo.get('country_code')

                        originCity = City(city=cityString,
                                          state=stateString,
                                          country=countryString)
                    else:
                        originCity.date = datetime.date.today()
                    originCity.save()

                    locations.append(str(locationCoordinates.get('latitude')) +
                                     ',' +
                                     str(locationCoordinates.get('longitude')))

                    # Save restaurant name and address
                    prettyName = ""
                    if len(displayAddress) > 0:
                        prettyName += displayAddress[0]
                    if len(displayAddress) > 1:
                        prettyName += ", "+displayAddress[1]
                    if len(displayAddress) > 2:
                        prettyName += ", "+displayAddress[2]
                    prettyLocations.append([item.get('name'),prettyName])

                    # Create bar entry in database
                    Bar(city=originCity,
                        name=item.get('name'),
                        address=prettyName,
                        lat=locationCoordinates.get('latitude'),
                        lng=locationCoordinates.get('longitude'),
                        priority=index).save()

            except urllib2.HTTPError as error:
                sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

    # ------
    # STEP 2 - Get distances between each restaurant
    # ------
    # Generate list of locations to visit in order
    url = 'https://maps.googleapis.com/maps/api/directions/json'

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
                   origin = locations[i],
                   destination = locations[j],
                   key = get_server_key()
               )

               # Set to 1 to skip later
               pairs[i][j] = 1
               pairs[j][i] = 1

               # Send request to Google Maps
               time.sleep(0.1)
               resp = requests.get(url=url, params=params)
               data = json.loads(resp.text)
               if (data.get('status') == 'ZERO_RESULTS'):
                   return {"status": 500,
                           "message": "Directions not found from " + prettyLocations[i][1]
                                         + " to " + prettyLocations[j][1]}
               else:
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

    cities_index = tsp_solver.solve_tsp(distances_matrix, 3)

    # Start and end cycle at start location
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
                  "route_addresses":[],
                  "status": 200}
    for item in cities_index:
        coordinates = locations[item].split(",")
        coordict = {"lat": float(coordinates[0]),
                    "lng": float(coordinates[1])}
        route_dict["route_coordinates"].append(coordict)
        route_dict["route_names"].append(prettyLocations[item][0])
        route_dict["route_addresses"].append(prettyLocations[item][1])

    return route_dict
