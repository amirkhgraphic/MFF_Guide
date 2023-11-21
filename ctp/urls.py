from django.urls import path
from ctp.views import scrape_ctp

urlpatterns = [
    path('scrape/', scrape_ctp),
]
