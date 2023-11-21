from django.urls import path
from card.views import scrape_card, fix_bug

urlpatterns = [
    path('scrape/', scrape_card),
    path('fix/', fix_bug),
]
