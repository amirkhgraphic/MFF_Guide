from django.urls import path
from apps.artifact.views import scrape_artifact

urlpatterns = [
    path('scrape/', scrape_artifact),
]
