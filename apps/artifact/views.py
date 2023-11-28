from django.shortcuts import HttpResponse
from django.template import loader

from apps.artifact.models import Artifact


def artifacts(request):
    template = loader.get_template("artifact/artifact.html")
    return HttpResponse(template.render({}, request))


def scrape_artifact(request):
    Artifact.scrape()
    return HttpResponse("DONE!")
