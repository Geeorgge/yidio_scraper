import os
import logging
import time
from yidio_scraper.models import YidioMovie as Movie
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

        # Fetch all and new links
        new_links, all_links = get_movie_links(url, file_name=output_file)

        # Save links without duplicates
        save_links_to_file(all_links, output_file)

        # Combine all links to process (existing + new)
        all_links = list(existing_links.union(unseen_links))

        # Process only new links
        unseen_links =  new_links

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

            # Save to DB if not exists
            movie, created = Movie.objects.get_or_create(
                title=movie_info.title.strip(),
                year=movie_info.year,
                length=(movie_info.length or '').strip(),
                defaults={
                    'image': movie_info.image,
                    'classification': movie_info.classification or '',
                    'imdb_rating': movie_info.imdb_rating or 0.0,
                    'description': movie_info.description or ''
                }
            )

            # Log results
            if created:
                movies_list.append(movie)
                logger.info(f"✅ New movie saved: {movie.title} ({movie.year})")
            else:
                logger.info(f"⚠️ Movie already exists: {movie.title} ({movie.year}) — skipped")


        # Save final results
        if movies_list:
            yidio_scraper.save_to_csv(movies_list)
            save_to_database(movies_list)
            for movie in movies_list:
                self.stdout.write(self.style.SUCCESS(f'Saved: {movie.title}'))

        self.stdout.write(self.style.SUCCESS("✅ Movie data extraction completed successfully."))
