from django.urls import path
from API.cardAPI.views import GetCardList, GetCardSearch


urlpatterns = [
    path('list/', GetCardList.as_view(), name='list-cards'),
    path('search/', GetCardSearch.as_view(), name='search-cards'),
]
