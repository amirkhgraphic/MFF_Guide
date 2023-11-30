from django.shortcuts import HttpResponse
from django.template import loader

from .models import CTP


def ctps(request):
    template = loader.get_template("ctp/ctps.html")
    return HttpResponse(template.render({}, request))


def scrape_ctp(request):
    CTP.scrape()
    return HttpResponse("done!!!!!!!!!!!!!!!!!!!!!!!")
