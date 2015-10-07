from django.http import HttpResponse
from django.shortcuts import render
import barcrawl

# Create your views here.
def index(request):
    return render(request, 'crawl/index.html', {})

def start(request):
    if request.POST:
        print("got here")
        start_address = request.POST['start_address']
        originInfo = barcrawl.get_origin(start_address)
        if originInfo:
            return HttpResponse("Valid Address")
        return HttpResponse("Not a searchable address! Please input a correct address")