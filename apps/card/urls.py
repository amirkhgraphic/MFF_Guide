from django.urls import path
from apps.card.views import scrape_card, fix_bug, cards

urlpatterns = [
    path('', cards),
    path('scrape/', scrape_card),
    path('fix/', fix_bug),
]
