from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, redirect
import barcrawl
import json

def index(request, context={}):
    if context == {}:
        context["actionURL"] = "/start/"

    return render(request, 'crawl/index.html', context)

def about(request, context={}):
    return render(request, 'crawl/about.html', context)

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
        for city in extra_cities:
            if (city != ''):
                try:
                    cities.index(city)
                    continue
                except ValueError:
                    cities.append(city)

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
            status = route["status"]
            if route["status"] == 200:
                route["status"] = "ok"

            return HttpResponse(json.dumps(route),
                                content_type="application/json",
                                status=status,
                                reason=route["status_text"])

#Bar Crawl within one city
def onecity(request):
    if request.POST:
        barcount = int(request.POST['barcount'])
        #PLACEHOLDER - EDIT TO BEGIN SEARCHING
        cities = [request.POST['origin_city']]
        #call barcrawl app
        route = barcrawl.main(cities, request.POST['start_address'], request.POST['origin_coordinates'], barcount)
        status = route["status"]
        if route["status"] == 200:
            route["status"] = "ok"

        return HttpResponse(json.dumps(route),
                            content_type="application/json",
                            status=status,
                            reason=route["status_text"])