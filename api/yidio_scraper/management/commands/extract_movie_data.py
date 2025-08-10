import os
import logging
import time
from yidio_scraper.models import YidioMovie as Movie
from django.core.management.base import BaseCommand
from yidio_scraper.commands.yidio_db import save_to_database
from yidio_scraper.commands.yidio_scraper import YidioScraper
from yidio_scraper.commands.yidio_get_links import get_movie_links

# Setup logger with console output
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
if not logger.hasHandlers():
    logger.addHandler(console_handler)

class Command(BaseCommand):
    help = 'Extracts movie data from Yidio and stores it in the database.'

    def handle(self, *args, **kwargs):
        url = "https://www.yidio.com/redesign/json/browse_results.php"
        output_file = "links.txt"

        logger.info("📥 Getting links from Yidio...")

        # Load existing links from file
        existing_links = set()
        if os.path.exists(output_file):
            with open(output_file, 'r') as file:
                existing_links = set(line.strip() for line in file if line.strip())

        # Fetch links (IMPORTANT: ensure the return order is correct)
        all_links, new_links = get_movie_links(url, file_name=output_file)

        if not all_links:
            logger.warning("No links found. Exiting.")
            return

        # Determine unseen new links
        unseen_links = set(new_links) - existing_links
        limited_links = list(unseen_links)

        if not limited_links:
            logger.warning("No new unseen links to process.")

            # Continue with all existing links instead
            limited_links = list(existing_links)
            logger.info(f"🔁 Proceeding with {len(limited_links)} previously saved links.")

        logger.info(f"🔗 Found {len(limited_links)} new links to process.")

        # Init scraper
        yidio_scraper = YidioScraper()
        movies_list = []

        for link in limited_links:
            logger.info(f"🎬 Processing movie: {link}")
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
                logger.warning(f"⚠️ Missing title or year in: {link} — skipping")
                continue

            # Save to DB if not exists
            movie, created = Movie.objects.update_or_create(
                title=movie_info.title.strip(),
                year=movie_info.year,
                length=(movie_info.length or '').strip(),
                defaults={
                'image': movie_info.image,
                'classification': movie_info.classification or '',
                'imdb_rating': float(movie_info.imdb_rating) if movie_info.imdb_rating else None,
                'description': movie_info.description or '',
                'tagline': movie_info.tagline or '',
                'genres': movie_info.genres or '',
                'cast': movie_info.cast or '',
                'director': movie_info.director or '',
                'where_to_watch': movie_info.where_to_watch or '',
                'mpaa_rating': movie_info.mpaa_rating or '',
                'metascore': int(movie_info.metascore) if movie_info.metascore and movie_info.metascore.isdigit() else None,
                'background_image': movie_info.background_image or yidio_scraper.extract_background_image_from_poster(movie_info.image, movie_info.movie_id)
            }
            )
            if created:
                movies_list.append(movie)
                logger.info(f"✅ Saved: {movie.title} ({movie.year})")
            else:
                # only update if mpaa_rating or metascore are present
                if movie_info.mpaa_rating or movie_info.metascore:
                    movie.mpaa_rating = movie_info.mpaa_rating
                    movie.metascore = movie_info.metascore
                    movies_list.append(movie)
                    logger.info(f"♻️ Update queued for: {movie.title} ({movie.year})")
                else:
                    logger.info(f"↪️ Already exists: {movie.title} ({movie.year})")

            # Save to CSV if needed
            if movies_list:
                yidio_scraper.save_to_csv(movies_list)
                save_to_database(movies_list)

        self.stdout.write(self.style.SUCCESS("✅ Movie data extraction completed successfully."))
