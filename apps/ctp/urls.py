from django.urls import path
from apps.ctp.views import scrape_ctp

urlpatterns = [
    path('scrape/', scrape_ctp),
]
