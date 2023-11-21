from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ctp/', include('ctp.urls')),
    path('card/', include('card.urls')),
    path('character/', include('character.urls')),
    path('artifact/', include('artifact.urls')),
    path('', include('home.urls')),
]
