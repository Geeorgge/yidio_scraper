from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('yidio_scraper.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
