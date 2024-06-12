from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=512)
    classification = models.CharField(max_length=10, default="NR", null=True, blank=True)
    year = models.IntegerField()
    length = models.CharField(max_length=20, null=True, blank=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    description = models.TextField()

class Meta:
        db_table = 'movies'

def __str__(self):
    return self.title
