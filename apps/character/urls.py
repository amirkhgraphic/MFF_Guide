from django.urls import path
from apps.character.views import scrape_character, fix_bug, list_characters

urlpatterns = [
    path('', list_characters),
    path('scrape/', scrape_character),
    path('fix/', fix_bug),
]
