from django.urls import path
from apps.character.views import scrape_character, fix_bug

urlpatterns = [
    path('scrape/', scrape_character),
    path('fix/', fix_bug),
]
