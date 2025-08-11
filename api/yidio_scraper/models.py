from django.db import models

class YidioMovie(models.Model):
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=512)
    background_image = models.CharField(max_length=512, null=True, blank=True)
    tagline = models.CharField(max_length=512, null=True, blank=True)
    classification = models.CharField(max_length=10, default="NR", null=True, blank=True)
    mpaa_rating = models.CharField(max_length=10, null=True, blank=True)
    year = models.IntegerField()
    length = models.CharField(max_length=20, null=True, blank=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    metascore = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    genres = models.TextField(null=True, blank=True)
    cast = models.TextField(null=True, blank=True)
    director = models.TextField(null=True, blank=True)
    where_to_watch = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'yidio_scraper_movie'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'year', 'length'],
                name='yidio_scraper_movie_title_year_length_uniq'
            )
        ]

    def __str__(self):
        return self.title