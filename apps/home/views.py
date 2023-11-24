from django.shortcuts import HttpResponse
from django.template import loader


def home(request):
    template = loader.get_template("home/home.html")

    context = {}
    return HttpResponse(template.render(context, request))
