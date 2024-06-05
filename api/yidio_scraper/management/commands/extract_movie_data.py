from yidio_scraper.models import Movie
from django.core.management.base import BaseCommand
from yidio_scraper.commands.yidio_db import save_to_database
from yidio_scraper.commands.yidio_scraper import YidioScraper
from yidio_scraper.commands.yidio_get_links import get_movie_links, save_links_to_file

# Class to execute the scraper movie as a django command
class Command(BaseCommand):
    help = 'Extracts movie data and saves it to the database'

    def handle(self, *args, **kwargs):
        url = "https://www.yidio.com/redesign/json/browse_results.php"
        links = get_movie_links(url)
        output_file = "links.txt"
        save_links_to_file(links, output_file)

        yidio_scraper = YidioScraper()
        movies_list = []

        with open(output_file, 'r') as file:
            movie_links = file.readlines()

        for link in movie_links:
            link = link.strip()
            movie_info = yidio_scraper.get_movie_info(link)
            if movie_info:
                movie = Movie(
                    title=movie_info.title,
                    image=movie_info.image,
                    classification=movie_info.classification,
                    year=movie_info.year,
                    length=movie_info.length,
                    imdb_rating=movie_info.imdb_rating,
                    description=movie_info.description
                )
                movie.save()
                movies_list.append(movie)
                
                
        if movies_list:
            yidio_scraper.save_to_csv(movies_list)
            save_to_database(movie)
            for movie in movies_list:
                self.stdout.write(self.style.SUCCESS(f'Successfully saved movie: {movie.title}'))

            

        self.stdout.write(self.style.SUCCESS("Movie data population complete!"))
