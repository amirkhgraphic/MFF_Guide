from django.shortcuts import HttpResponse
from apps.artifact.models import Artifact


def scrape_artifact(request):
    Artifact.scrape()
    return HttpResponse("DONE!")
