from django.urls import path
from API.cardAPI.views import GetCardList

urlpatterns = [
    path('list/', GetCardList.as_view(), name='list-card'),
]
