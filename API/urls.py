from django.urls import path, include

urlpatterns = [
    path('character/', include('API.characterAPI.urls')),
]
