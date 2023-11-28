from django.urls import path
from apps.character.views import scrape_character, fix_bug, characters

urlpatterns = [
    path('', characters),
    path('scrape/', scrape_character),
    path('fix/', fix_bug),
]
