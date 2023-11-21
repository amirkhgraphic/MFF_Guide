from django.urls import path
from character.views import scrape_character

urlpatterns = [
    path('scrape/', scrape_character),
]
