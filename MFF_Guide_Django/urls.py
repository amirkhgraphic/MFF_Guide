from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ctp/', include('apps.ctp.urls')),
    path('card/', include('apps.card.urls')),
    path('character/', include('apps.character.urls')),
    path('artifact/', include('apps.artifact.urls')),
    path('', include('apps.home.urls')),
    path('api/', include('API.urls')),
]
