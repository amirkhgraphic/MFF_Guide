from django.shortcuts import HttpResponse
from artifact.models import Artifact


def scrape_artifact(request):
    Artifact.scrape()
    return HttpResponse("DONE!")
