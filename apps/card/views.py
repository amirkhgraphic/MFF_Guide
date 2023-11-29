from django.shortcuts import HttpResponse
from django.template import loader
from apps.card.models import Card


def cards(request):
    template = loader.get_template("card/cards.html")
    return HttpResponse(template.render({}, request))


def scrape_card(request):
    Card.scrape()
    return HttpResponse("DONE!")


def fix_bug(request):
    problematics = Card.objects.filter(name__contains="&amp;")

    for record in problematics:
        record.name = record.name.replace("&amp;", "&")
        record.save()

    return HttpResponse("DONE!")
