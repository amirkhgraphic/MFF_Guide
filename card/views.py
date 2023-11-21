from django.shortcuts import HttpResponse
from card.models import Card


def scrape_card(request):
    Card.scrape()
    return HttpResponse("DONE!")


def fix_bug(request):
    problematics = Card.objects.filter(name__contains="&amp;")

    for record in problematics:
        record.name = record.name.replace("&amp;", "&")
        record.save()

    return HttpResponse("DONE!")
