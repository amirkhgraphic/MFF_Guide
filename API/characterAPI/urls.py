from django.urls import path
from API.characterAPI.views import GetCharacterList, GetCharacterDetail

urlpatterns = [
    path('list/', GetCharacterList.as_view(), name='list-characters'),
    path('retrieve/<int:pk>', GetCharacterDetail.as_view(), name='retrieve-character'),
]
