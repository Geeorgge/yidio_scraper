import os
import logging
import time
from yidio_scraper.models import Movie
from django.core.management.base import BaseCommand
from yidio_scraper.commands.yidio_db import save_to_database
from yidio_scraper.commands.yidio_scraper import YidioScraper
from yidio_scraper.commands.yidio_get_links import get_movie_links, save_links_to_file

# Set up a logger for this command
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Extracts movie data from Yidio and stores it in the database.'

    def handle(self, *args, **kwargs):
        url = "https://www.yidio.com/redesign/json/browse_results.php"
        output_file = "links.txt"

        # Load existing links from file
        existing_links = set()
        if os.path.exists(output_file):
            with open(output_file, 'r') as file:
                existing_links = set(line.strip() for line in file if line.strip())

        # Fetch new links and filter only the unseen ones
        new_links = get_movie_links(url, file_name=output_file)
        unseen_links = [link for link in new_links if link not in existing_links]

        # Save only unseen links to file
        save_links_to_file(unseen_links, output_file)

        # Combine all links to process (existing + new)
        all_links = list(existing_links.union(unseen_links))

        # Init scraper
        yidio_scraper = YidioScraper()
        movies_list = []

        # Loop through all links
        for link in all_links:
            logger.info(f"Processing movie page: {link}")
            movie_info = None

            for attempt in range(3):
                try:
                    movie_info = yidio_scraper.get_movie_info(link)
                    if movie_info:
                        break
                except Exception as e:
                    logger.warning(f"Attempt {attempt+1} failed for {link}: {e}")
                    time.sleep(2)

            if not movie_info:
                logger.error(f"Failed to extract info from: {link}")
                continue

            if not movie_info.title or not movie_info.year:
                logger.warning(f"Missing title or year in: {link} — skipping")
                continue

            if Movie.objects.filter(title=movie_info.title, year=movie_info.year).exists():
                logger.info(f"Movie already exists in DB: {movie_info.title} ({movie_info.year})")
                continue

            movie = Movie(
                title=movie_info.title,
                image=movie_info.image,
                classification=movie_info.classification or '',
                year=movie_info.year,
                length=movie_info.length or '',
                imdb_rating=movie_info.imdb_rating or None,
                description=movie_info.description or ''
            )
            movie.save()
            movies_list.append(movie)
            logger.info(f"Saved movie: {movie.title} ({movie.year})")

        # Save final results
        if movies_list:
            yidio_scraper.save_to_csv(movies_list)
            save_to_database(movies_list)
            for movie in movies_list:
                self.stdout.write(self.style.SUCCESS(f'Saved: {movie.title}'))

        self.stdout.write(self.style.SUCCESS("✅ Movie data extraction completed successfully."))
