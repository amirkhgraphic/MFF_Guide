from django.urls import path, include

urlpatterns = [
    path('character/', include('API.characterAPI.urls')),
    path('artifact/', include('API.artifactAPI.urls')),
    path('card/', include('API.cardAPI.urls')),
    path('ctp/', include('API.ctpAPI.urls')),
]
