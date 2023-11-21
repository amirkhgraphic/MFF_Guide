from django.shortcuts import HttpResponse
from .models import CTP

def scrape_ctp(request):
    CTP.scrape()
    return HttpResponse("done!!!!!!!!!!!!!!!!!!!!!!!")
