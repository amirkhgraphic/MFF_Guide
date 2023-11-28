from django.urls import path
from apps.artifact.views import scrape_artifact, artifacts

urlpatterns = [
    path('', artifacts),
    path('scrape/', scrape_artifact),
]
