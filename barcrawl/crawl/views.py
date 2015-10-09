from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import barcrawl
import json

def index(request, context={}):
    if context == {}:
        context["actionURL"] = "/start/"

    return render(request, 'crawl/index.html', context)

#Get origin address
def start(request):
    if request.POST:
        start_address = request.POST['start_address']
        #Get coordinates of origin
        originInfo = barcrawl.get_origin(start_address)
        if originInfo:
            response = json.dumps({"relinquish":"cities",
                                   "action":"/cities/",
                                   "origin_city":originInfo["city"],
                                   "origin_coordinates":originInfo["coordinates"]})

            return HttpResponse(response, content_type="application/json")
        else:
            response = json.dumps({"Not a searchable address": "Please input a correct address"})
            #Origin address could not be found
            return HttpResponse(response,
                                content_type="application/json",
                                status_code=401)
#Get list of cities
def cities(request):
    if request.POST:
        #Establish origin city as first city
        cities = [request.POST['origin_city']]

        #Get other cities
        extra_cities = request.POST['cities'].split(",")
        if len(extra_cities) > 0 and extra_cities[0] != '':
            cities += extra_cities

        #Only listed one city
        if (len(cities) == 1):
            #Prompt for number of bars to visit
            return HttpResponse(json.dumps({"relinquish":"barcount",
                                            "action":"/onecity/",
                                            "origin_city":request.POST['origin_city'],
                                            "origin_coordinates":request.POST['origin_coordinates']}),
                                content_type="application/json")

        else:
            #call barcrawl app
            route = barcrawl.main(cities, request.POST['start_address'], request.POST['origin_coordinates'])

            route["status"] = "ok";
            #PLACEHOLDER - EDIT TO BEGIN SEARCHING
            return HttpResponse(json.dumps(route),
                                content_type="application/json")

#Bar Crawl within one city
def onecity(request):
    if request.POST:
        barcount = int(request.POST['barcount'])
        #PLACEHOLDER - EDIT TO BEGIN SEARCHING
        cities = [request.POST['origin_city']]
        #call barcrawl app
        route = barcrawl.main(cities, request.POST['start_address'], request.POST['origin_coordinates'], barcount)

        route["status"] = "ok";
        #PLACEHOLDER - EDIT TO BEGIN SEARCHING
        return HttpResponse(json.dumps(route),
                            content_type="application/json")