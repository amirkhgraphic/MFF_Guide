from django.shortcuts import HttpResponse
from apps.character.models import Character


def scrape_character(request):
    Character.scrape()
    return HttpResponse("DONE!")


def fix_bug(request):
    problematics = Character.objects.filter()

    for item in problematics:
        s = item.advancement.strip('[').strip(']')
        item.advancement = list(s.split(', '))[-1].strip("'").strip('"')
        item.save()

    return HttpResponse("DONE!")
