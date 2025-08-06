from .views import MovieListAPIView
from django.urls import path, include
from .views import MovieViewSet, movie_list
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('api/movies/', MovieListAPIView.as_view(), name='movie-list'),
    path('movies/', movie_list, name='movie_list.html'),
]
