from .views import YidioMovieListAPIView, YidioMovieViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'yidio-movies', YidioMovieViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/yidio-movie-list/', YidioMovieListAPIView.as_view(), name='yidio-movie-list'),
]