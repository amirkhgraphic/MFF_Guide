from django.urls import path
from API.artifactAPI.views import GetArtifactList, GetArtifactSearch


urlpatterns = [
    path('list/', GetArtifactList.as_view(), name='list-artifacts'),
    path('search/', GetArtifactSearch.as_view(), name='search-artifacts'),
]
