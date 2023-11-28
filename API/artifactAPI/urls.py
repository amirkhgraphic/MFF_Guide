from django.urls import path
from API.artifactAPI.views import GetArtifactList

urlpatterns = [
    path('list/', GetArtifactList.as_view(), name='list-artifacts'),
]
