from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, movie_list

router = DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('movies/', movie_list, name='movie_list.html'),
]
