from .models import Movie
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import MovieSerializer
from rest_framework import generics
from rest_framework.filters import SearchFilter

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

def movie_list(request):
    movies = Movie.objects.all()[:10]  # Get the first 10 movies
    return render(request, 'movie_list.html', {'movies': movies})

class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']
