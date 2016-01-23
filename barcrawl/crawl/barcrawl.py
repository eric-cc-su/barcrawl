# CS4800 - Mini Pacman Bar Hopping
# Input:   Cities to visit
# Output:  Route to the highest rated bar in each city

import datetime
import json, requests # for making request to Google Maps
import os
import urllib2, sys, time
import yelp
import tsp_solver

from django.db.models import Q
from django.http import HttpResponse
from crawl.models import City, Bar, Distance

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
        returnDict = {"coordinates": '{},{}'.format(str(lat),str(lng)),
                      "city": city}
    except:
        return False
    return(returnDict)

# Removes any bars from database with priority 0
def bar_cleanup():
    cleanup = Bar.objects.filter(priority=0)

    # Remove distance entries referring to Bar
    for bar in cleanup:
        Distance.objects.filter(Q(start=bar) | Q(end=bar)).delete()

    cleanup.delete()

# Get bars in each city
def get_bars(cities, locations, prettyLocations, search_limit):
    # Get list of top restaurants in each city
    for city in cities:
        createCity = False

        # Handle naming exception for New York City
        if (city.lower().strip() == "new york city"):
            city = "new york"

        # SELECT * FROM crawl_city WHERE city = city.lower()
        try:
            originCity = City.objects.get(city=city.lower().strip())

        except City.DoesNotExist:
            originCity = City(city=city.lower())
            originCity.save()
            createCity = True

        # Calculate last update of city info
        datedelta = (datetime.date.today() - originCity.date).days

        # City exists in database and is up to date
        # and is associated with enough bars
        if datedelta < 31 \
        and Bar.objects.filter(city=originCity).count() >= search_limit:
            # SELECT * FROM crawl_bar
            # WHERE city_id = originCity
            # ORDER BY priority ASC
            # LIMIT search_limit
            bars = (Bar.objects.filter(city=originCity)
                        .order_by('priority')[:search_limit])

            for item in bars:
                locations.append((item.id, str(item.lat)+','+str(item.lng)))
                prettyLocations.append([item.name,item.address])

        else:
            try:
                response = yelp.query_api('bars', city, search_limit)

                # Iterate through bars received from request
                for index, item in response:
                    locationInfo = item.get('location')
                    locationCoordinates = locationInfo.get('coordinate')
                    displayAddress = locationInfo.get('display_address')

                    # City does not exist in database
                    if createCity:
                        cityString = locationInfo.get('city').lower()
                        stateString = locationInfo.get('state_code')
                        countryString = locationInfo.get('country_code')

                        originCity.city = cityString
                        originCity.state = stateString
                        originCity.country = countryString
                        createCity = False

                    # Mark city as up-to-date
                    if datedelta >= 31:
                        originCity.date = datetime.date.today()
                        originCity.save()

                    originCity.save()

                    # construct bar address
                    prettyName = ""
                    if len(displayAddress) > 0:
                        prettyName += displayAddress[0]
                    if len(displayAddress) > 1:
                        prettyName += ", "+displayAddress[1]
                    if len(displayAddress) > 2:
                        prettyName += ", "+displayAddress[2]
                    prettyLocations.append([item.get('name'),prettyName])

                    # Check if the bar exists in the database
                    try:
                        attemptBar = Bar.objects.get(city=originCity,
                                     name=item.get('name'),
                                     address=prettyName,
                                     lat=locationCoordinates.get('latitude'),
                                     lng=locationCoordinates.get('longitude'))

                        # Update bar's priority if needed
                        if (attemptBar.priority != index):
                            attemptBar.priority = index
                            attemptBar.save()

                    # Bar does not exist in database
                    # Create bar entry in database
                    except Bar.DoesNotExist:
                        # Get bars that currently hold the priority placement
                        conflictBars = (Bar.objects.filter(city=originCity,
                                                          priority=index)
                                .exclude(Q(name=item.get('name')) |
                                  Q(address=prettyName) |
                                  Q(lat=locationCoordinates.get('latitude')) |
                                  Q(lng=locationCoordinates.get('longitude'))))
                        # Update conflicting bars to priority 0
                        for bar in conflictBars:
                            bar.priority=0
                            bar.save()

                        # Create new bar object and save
                        attemptBar = Bar(city=originCity,
                                     name=item.get('name'),
                                     address=prettyName,
                                     lat=locationCoordinates.get('latitude'),
                                     lng=locationCoordinates.get('longitude'),
                                     priority=index)
                        attemptBar.save()

                    locations.append((attemptBar,
                                  str(locationCoordinates.get('latitude')) +
                                  ',' +
                                  str(locationCoordinates.get('longitude'))))

            except urllib2.HTTPError as error:
                sys.exit('Encountered HTTP error {0}. Abort program.'
                         .format(error.code))
    # Remove bars with priority 0 from database
    bar_cleanup()

def get_distances(locations, prettyLocations):
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
            requestDistance = True

            # Skip over duplicate pairs of locations to reduce requests
            if pairs[i][j] != 1 and i != j:
                distanceData = None
                if locations[i][0] != 0 and locations[j][0] != 0:

                    try:
                        # Find distance entry in database
                        distanceData = Distance.objects.get(
                            start = locations[i][0],
                            end = locations[j][0])
                        requestDistance = False

                    except Distance.DoesNotExist:
                        # Create new distance entry
                        distanceData = Distance(
                            start = locations[i][0],
                            end = locations[j][0],
                            distance = 0
                        )
                        distanceData.save()

                # Set to 1 to skip later
                pairs[i][j] = 1
                pairs[j][i] = 1

                # Need to send request for distance data
                if requestDistance:
                    # Set parameters
                    if len(locations[i]) == 1:
                        paramOrigin = locations[i]
                    else:
                        paramOrigin = locations[i][1]

                    if len(locations[j]) == 1:
                        paramDest = locations[j]
                    else:
                        paramDest = locations[j][1]

                    params = dict(
                        origin = paramOrigin,
                        destination = paramDest,
                        key = get_server_key()
                    )
                    # Send request to Google Maps
                    time.sleep(0.1) # limit GMap request rate
                    resp = requests.get(url=url, params=params)
                    data = json.loads(resp.text)
                    if (data.get('status') == 'ZERO_RESULTS'):
                        return {"status": 500,
                                "message": "Directions not found from "+
                                           prettyLocations[i][1]+
                                           " to " + prettyLocations[j][1]}
                    else:
                        distanceResponse = (data.get('routes')[0]
                                            .get('legs')[0]
                                            .get('distance')
                                            .get('value'))

                        # Store distance in database
                        # ONLY if distance is between bars
                        if distanceData:
                            distanceData.distance = distanceResponse
                            distanceData.save()

                        # Storing distances in matrix for tsp_solver
                        distances_matrix[i][j] = distanceResponse
                        distances_matrix[j][i] = distanceResponse

                # Distance exists in database
                else:
                    distances_matrix[i][j] = distanceData.distance
                    distances_matrix[j][i] = distanceData.distance

                counter += 1
                sys.stdout.write("\rGetting Distances...%d%%" %
                                 int((float(counter)/lookupNum) * 100))
                sys.stdout.flush()

    return distances_matrix

# ------
# STEP 1 - Get top restaurants
# ------
def main(cities, origin_address, origin_coordinates, search_limit=1):
    # coordinates of locations
    locations = []
    # User-friendly Addresses
    prettyLocations = []

    locations.append((0, origin_coordinates))
    prettyLocations.append(['Origin',origin_address])

    returnedException = None

    try:
        get_bars(cities, locations, prettyLocations, search_limit)


        # ------
        # STEP 2 - Get distances between each restaurant
        # ------
        # Generate list of locations to visit in order
        distances_matrix = get_distances(locations, prettyLocations)
    except Exception as e:
        print(e)
        return HttpResponse(e, status=500, reason=e)
        #returnedException = e
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

    status = 200
    status_text = ""
    if returnedException:
        status = 500
        status_text = returnedException

    route_dict = {"origin_coordinates":{"lat": float(origin_coordinates
                                                     .split(",")[0]),
                                        "lng": float(origin_coordinates
                                                     .split(",")[1])},
                  "route_coordinates":[],
                  "route_names":[],
                  "route_addresses":[],
                  "status": status,
                  "status_text": status_text}
    for item in cities_index:
        coordinates = locations[item][1].split(",")
        coordict = {"lat": float(coordinates[0]),
                    "lng": float(coordinates[1])}
        route_dict["route_coordinates"].append(coordict)
        route_dict["route_names"].append(prettyLocations[item][0])
        route_dict["route_addresses"].append(prettyLocations[item][1])

    return route_dict