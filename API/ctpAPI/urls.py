from django.urls import path
from API.ctpAPI.views import GetCTPList, GetCTPSearch


urlpatterns = [
    path('list/', GetCTPList.as_view(), name='list-ctp'),
    path('search/', GetCTPSearch.as_view(), name='search-ctp'),
]
