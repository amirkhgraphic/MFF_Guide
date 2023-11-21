from django.shortcuts import HttpResponse
from character.models import Character


def scrape_character(request):
    Character.scrape()
    return HttpResponse("DONE!")
