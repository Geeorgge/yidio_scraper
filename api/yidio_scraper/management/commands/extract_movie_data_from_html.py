import os
import logging
import time
from yidio_scraper.models import YidioMovie as Movie
from django.core.management.base import BaseCommand
from yidio_scraper.commands.yidio_db import save_to_database
from yidio_scraper.commands.yidio_scraper import YidioScraper

# Setup logger with console output
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
if not logger.hasHandlers():
    logger.addHandler(console_handler)

class Command(BaseCommand):
    help = 'Extracts movie data from local HTML files and stores it in the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--html-dir',
            type=str,
            default='/api/movie_htmls',
            help='Directory containing HTML files to process'
        )
        parser.add_argument(
            '--processed-file',
            type=str,
            default='processed_files.txt',
            help='File to track processed HTML files (default: processed_files.txt)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of movies to process before saving to database (default: 100)'
        )
        parser.add_argument(
            '--max-files',
            type=int,
            default=None,
            help='Maximum number of files to process (for testing, default: process all)'
        )

    def get_html_files(self, html_dir):
        """Get all HTML files from the specified directory"""
        if not os.path.exists(html_dir):
            logger.error(f"HTML directory does not exist: {html_dir}")
            return []
        
        html_files = []
        for root, dirs, files in os.walk(html_dir):
            for file in files:
                if file.lower().endswith(('.html', '.htm')):
                    html_files.append(os.path.join(root, file))
        
        logger.info(f"📂 Found {len(html_files)} HTML files in {html_dir}")
        return html_files

    def load_processed_files(self, processed_file):
        """Load list of already processed files"""
        processed_files = set()
        if os.path.exists(processed_file):
            with open(processed_file, 'r') as file:
                processed_files = set(line.strip() for line in file if line.strip())
        return processed_files

    def save_processed_file(self, processed_file, filename):
        """Save a processed file to the tracking file"""
        with open(processed_file, 'a') as file:
            file.write(f"{filename}\n")

    def handle(self, *args, **kwargs):
        html_dir = kwargs.get("html_dir", "movie_htmls")
        processed_file = kwargs['processed_file']
        batch_size = kwargs['batch_size']
        max_files = kwargs['max_files']

        logger.info(f"📥 Getting HTML files from {html_dir}...")
        logger.info(f"⚙️  Batch size: {batch_size}, Max files: {max_files or 'All'}")

        # Get all HTML files
        all_html_files = self.get_html_files(html_dir)
        
        if not all_html_files:
            logger.warning("No HTML files found. Exiting.")
            return

        logger.info(f"📂 Total HTML files found: {len(all_html_files)}")

        # Load processed files
        processed_files = self.load_processed_files(processed_file)
        logger.info(f"✅ Already processed: {len(processed_files)} files")

        # Determine unprocessed files
        unprocessed_files = [f for f in all_html_files if f not in processed_files]

        if not unprocessed_files:
            logger.warning("No new HTML files to process.")
            logger.info(f"🔁 All {len(all_html_files)} HTML files have been processed.")
            return

        # Limit files if max_files is specified (useful for testing)
        if max_files:
            unprocessed_files = unprocessed_files[:max_files]

        logger.info(f"🎯 Processing {len(unprocessed_files)} HTML files...")

        # Init scraper
        yidio_scraper = YidioScraper()
        movies_list = []
        processed_count = 0
        errors_count = 0

        for i, html_file in enumerate(unprocessed_files, 1):
            # Progress indicator
            if i % 100 == 0:
                logger.info(f"📊 Progress: {i}/{len(unprocessed_files)} files ({i/len(unprocessed_files)*100:.1f}%)")
            
            logger.debug(f"🎬 Processing [{i}/{len(unprocessed_files)}]: {os.path.basename(html_file)}")
            movie_info = None

            for attempt in range(2):  # Reduced attempts for performance
                try:
                    # Read HTML file content
                    with open(html_file, 'r', encoding='utf-8') as file:
                        html_content = file.read()
                    
                    # Debug: Check if file was read
                    print(f"DEBUG - File size: {len(html_content)} chars")
                    
                    # Extract movie info from HTML content
                    movie_info = yidio_scraper.extract_movie_info_from_html(html_content, html_file)
                    
                    if movie_info:
                        break
                except Exception as e:
                    logger.debug(f"Attempt {attempt+1} failed for {os.path.basename(html_file)}: {e}")
                    import traceback
                    traceback.print_exc()  # Show full error trace
                    if attempt == 0:  # Only sleep on first failure
                        time.sleep(0.5)

            if not movie_info:
                logger.debug(f"❌ Failed to extract info from: {os.path.basename(html_file)}")
                errors_count += 1
                self.save_processed_file(processed_file, html_file)
                continue

            if not movie_info.title or not movie_info.year:
                logger.debug(f"⚠️ Missing title or year in: {os.path.basename(html_file)} — skipping")
                self.save_processed_file(processed_file, html_file)
                continue

            try:
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
                    logger.debug(f"✅ Saved: {movie.title} ({movie.year})")
                else:
                    # only update if mpaa_rating or metascore are present
                    if movie_info.mpaa_rating or movie_info.metascore:
                        movie.mpaa_rating = movie_info.mpaa_rating or movie.mpaa_rating
                        movie.metascore = int(movie_info.metascore) if movie_info.metascore and movie_info.metascore.isdigit() else movie.metascore
                        movie.save()
                        movies_list.append(movie)
                        logger.debug(f"♻️ Updated: {movie.title} ({movie.year})")
                    else:
                        logger.debug(f"↪️ Already exists: {movie.title} ({movie.year})")

                # Mark as processed
                self.save_processed_file(processed_file, html_file)
                processed_count += 1

                # Save to CSV and DB in batches
                if len(movies_list) >= batch_size:
                    logger.info(f"💾 Saving batch of {len(movies_list)} movies to database...")
                    yidio_scraper.save_to_csv(movies_list)
                    save_to_database(movies_list)
                    movies_list = []  # Clear the list after saving

            except Exception as e:
                logger.error(f"Error saving movie from {os.path.basename(html_file)}: {e}")
                errors_count += 1
                self.save_processed_file(processed_file, html_file)

        # Save any remaining movies
        if movies_list:
            logger.info(f"💾 Saving final batch of {len(movies_list)} movies...")
            yidio_scraper.save_to_csv(movies_list)
            save_to_database(movies_list)

        logger.info(f"🎯 Successfully processed: {processed_count} files")
        logger.info(f"❌ Errors encountered: {errors_count} files")
        logger.info(f"📊 Total completion: {processed_count + errors_count}/{len(unprocessed_files)}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Completed! Processed {processed_count} movies, {errors_count} errors."
            )
        )