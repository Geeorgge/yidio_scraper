from .models import YidioMovie
from django.shortcuts import render
from rest_framework import viewsets, filters, generics
from .serializers import YidioMovieSerializer
from rest_framework import generics
from rest_framework.filters import SearchFilter

# Create your views here.
class YidioMovieViewSet(viewsets.ModelViewSet):
    queryset = YidioMovie.objects.all()
    serializer_class = YidioMovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'classification']

def movie_list(request):
    movies = YidioMovie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

class YidioMovieListAPIView(generics.ListAPIView):
    queryset = YidioMovie.objects.all()
    serializer_class = YidioMovieSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']
