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
            return HttpResponse(json.dumps({"relinquish":"cities",
                                            "action":"/cities/"}),
                                content_type="application/json")
        else:
            #Origin address could not be found
            return HttpResponse(json.dumps({"Not a searchable address": "Please input a correct address"}),
                                content_type="application/json",
                                status_code=401)
#Get list of cities
def cities(request):
    if request.POST:
        cities = request.POST['cities'].split(",")
        print(cities)
        #Only listed one city
        if (len(cities) == 1):
            #Prompt for number of bars to visit
            return HttpResponse(json.dumps({"relinquish":"barcount",
                                            "action":"/onecity/"}),
                                content_type="application/json")

        #PLACEHOLDER - EDIT TO BEGIN SEARCHING
        return HttpResponse(json.dumps({"status":"ok"}),
                            content_type="application/json")

#Bar Crawl within one city
def onecity(request):
    if request.POST:
        barcount = request.POST['barcount']
        #PLACEHOLDER - EDIT TO BEGIN SEARCHING
        return HttpResponse(json.dumps({"status":"ok"}),
                            content_type="application/json")