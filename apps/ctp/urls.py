from django.urls import path
from apps.ctp.views import scrape_ctp, ctps

urlpatterns = [
    path('', ctps),
    path('scrape/', scrape_ctp),
]
