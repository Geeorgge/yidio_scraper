from rest_framework import serializers
from .models import YidioMovie

class YidioMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = YidioMovie
        fields = '__all__'
