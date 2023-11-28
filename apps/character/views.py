from django.shortcuts import HttpResponse
from django.template import loader
from .models import Character


def characters(request):
    template = loader.get_template("character/characters.html")
    context = {}
    return HttpResponse(template.render(context, request))


def scrape_character(request):
    if input('enter y to continue...') == 'y':
        Character.scrape()
    return HttpResponse("DONE!")


def fix_bug(request):
    problematics = Character.objects.filter()

    for item in problematics:
        s = item.advancement.strip('[').strip(']')
        item.advancement = list(s.split(', '))[-1].strip("'").strip('"')
        item.save()

    return HttpResponse("DONE!")
