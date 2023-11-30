from django.urls import path
from API.ctpAPI.views import GetCTPList

urlpatterns = [
    path('list/', GetCTPList.as_view(), name='list-ctp'),
]
