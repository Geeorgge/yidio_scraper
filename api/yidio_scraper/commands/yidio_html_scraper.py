import os
import re
import csv
from bs4 import BeautifulSoup
from yidio_scraper.models import YidioMovie


class YidioScraper:

    # Funct to extract the image movie
    def extract_image(self, soup):
        content_div = soup.find('div', class_='content')
        if content_div:
            image_tag = content_div.select_one('div.poster.movie img')
            if image_tag and 'src' in image_tag.attrs:
                image_src = image_tag['src'].strip()
                return image_src
        return None


    # Converts the poster image URL to the background image URL
    def extract_background_image_from_poster(self, poster_url, movie_id):
        if not poster_url or not movie_id:
            return None
        return f"https://cfm.yidio.com/images/movie/{movie_id}/backdrop-1280x720.jpg"


    # Funct to extract the title movie
    def extract_title(self, soup):
        content_div = soup.find('div', class_='content')
        if content_div:
            title_elem = content_div.select_one('div.details h1')
            if title_elem:
                title = title_elem.text.strip().replace('Watch ', '')
                return title
        return None
    

    # Function to extract the tagline
    def extract_tagline(self, soup):
        tagline_elem = soup.select_one("div.tagline")
        if tagline_elem:
            return tagline_elem.get_text(strip=True)
        return None
    
  
    # Funct to extract the classification movie
    def extract_classification(self, soup):
        classification_elem = soup.select_one('ul.attributes > li:nth-of-type(1)')
        if classification_elem:
            classification = classification_elem.text.strip()
            allowed_classifications = ["R", "PG-13", "PG", "G", "NC-17", "NR"]
            if classification not in allowed_classifications:
                classification = None 
            return classification
        return None 


    # Funct to extract the year movie
    def extract_year(self, soup):
        attributes = soup.select('ul.attributes > li')
        for li in attributes:
            text = li.text.strip()
            if re.match(r'^\d{4}$', text):
                return int(text)
        return None


    # Funct to extract the length movie
    def extract_length(self, soup):
        length_elem = soup.select_one('ul.attributes > li:nth-of-type(3)')
        if length_elem:
            length = length_elem.text.strip()
            if re.match(r'^\d+ hr \d+ min$', length):
                return length
        return None 


    # Funct to extract the imdb rating movie
    def extract_imdb_rating(self, soup):
        imdb_rating_div = soup.select_one('ul.attributes > li.imdb')
        if imdb_rating_div:
            imdb_rating_span = imdb_rating_div.select_one('span')
            if imdb_rating_span:
                imdb_rating_span.decompose()
            imdb_rating = imdb_rating_div.text.strip()
            try:
                imdb_rating_float = float(imdb_rating)
                return f"{imdb_rating_float:.1f}"
            except ValueError:
                pass
        return '0.0'


    # Funct to extract the description movie
    def extract_description(self, soup):
        description_elem = soup.select_one('div.description p')
        if description_elem:
            description_text = description_elem.text.strip()
            description_text = re.sub(r'[^ -~]', '', description_text)
            try:
                description = description_text.encode('utf-8').decode('utf-8')
                return description
            except UnicodeEncodeError as e:
                print("Error de codificación:", e)
        return ''


    # Function to extract where to watch (with fallback text)
    def extract_where_to_watch(self, soup):
        where_to_watch_div = soup.find("div", class_="where-to-watch")
        if where_to_watch_div:
            value_div = where_to_watch_div.find("div", class_="value")
            if value_div:
                return value_div.get_text(strip=True)
        return "doesn't appear to be available from any streaming services."


    # Function to extract genres
    def extract_genres(self, soup):
        links_section = soup.select_one("ul.links")
        if links_section:
            for li in links_section.find_all("li"):
                name = li.find("div", class_="name")
                if name and name.get_text(strip=True).lower() == "genres":
                    return [el.get_text(strip=True) for el in li.select("div.value a") if el.get_text(strip=True)]
        return []


    # Function to extract cast
    def extract_cast(self, soup):
        links_section = soup.select_one("ul.links")
        if links_section:
            for li in links_section.find_all("li"):
                name = li.find("div", class_="name")
                if name and name.get_text(strip=True).lower() == "cast":
                    return [el.get_text(strip=True) for el in li.select("div.value div") if el.get_text(strip=True)]
        return []


    # Function to extract director
    def extract_director(self, soup):
        links_section = soup.select_one("ul.links")
        if links_section:
            for li in links_section.find_all("li"):
                name = li.find("div", class_="name")
                if name and name.get_text(strip=True).lower() == "director":
                    return [el.get_text(strip=True) for el in li.select("div.value div") if el.get_text(strip=True)]
        return []

    # New methods to extract MPAA rating and Metascore from HTML content
    def extract_mpaa_rating_from_html(self, soup):

        try:
            # Common patterns where MPAA rating might be found
            # Adjust these selectors based on your HTML structure
            
            # Method 1: Look for specific classes/IDs
            mpaa_element = soup.find(class_=re.compile('mpaa|rating', re.I))
            if mpaa_element:
                return mpaa_element.get_text().strip()
            
            # Method 2: Look for text patterns
            text_content = soup.get_text()
            mpaa_match = re.search(r'\b(G|PG|PG-13|R|NC-17|NR|Not Rated)\b', text_content)
            if mpaa_match:
                return mpaa_match.group(1)
            
            # Method 3: Look in meta tags
            meta_rating = soup.find('meta', attrs={'name': re.compile('rating', re.I)})
            if meta_rating and meta_rating.get('content'):
                return meta_rating['content']
                
        except Exception as e:
            print(f"Error extracting MPAA rating: {e}")
        
        return None

    def extract_metascore_from_html(self, soup):
        """
        Try to extract Metascore from HTML content
        """
        try:
            # Common patterns where Metascore might be found
            
            # Method 1: Look for Metacritic specific classes
            meta_element = soup.find(class_=re.compile('metascore|metacritic', re.I))
            if meta_element:
                score_text = meta_element.get_text().strip()
                score_match = re.search(r'\d+', score_text)
                if score_match:
                    return score_match.group()
            
            # Method 2: Look for numeric patterns near "Metascore" or "Metacritic"
            text_content = soup.get_text()
            metascore_match = re.search(r'(?:Metascore|Metacritic).*?(\d+)', text_content, re.I)
            if metascore_match:
                return metascore_match.group(1)
            
            # Method 3: Look in data attributes
            for elem in soup.find_all(attrs={'data-metascore': True}):
                return elem['data-metascore']
                
        except Exception as e:
            print(f"Error extracting Metascore: {e}")
        
        return None

    def extract_movie_info_from_html(self, html_content, file_path=None):
        try:
            # Parse HTML content directly
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract all movie attributes using existing methods
            image = self.extract_image(soup)
            title = self.extract_title(soup)
            classification = self.extract_classification(soup)
            year = self.extract_year(soup)
            length = self.extract_length(soup)
            imdb_rating = self.extract_imdb_rating(soup)
            description = self.extract_description(soup)
            tagline = self.extract_tagline(soup)
            where_to_watch = self.extract_where_to_watch(soup)
            genres = self.extract_genres(soup)
            cast = self.extract_cast(soup)
            director = self.extract_director(soup)
            mpaa_rating = self.extract_mpaa_rating_from_html(soup)
            metascore = self.extract_metascore_from_html(soup)

            # Extract movie ID from file name (if it contains digits)
            movie_id = None
            if file_path:
                match = re.search(r'(\d+)', os.path.basename(file_path))
                movie_id = match.group(1) if match else None

            # Optional background image
            background_image = None
            if image and movie_id:
                try:
                    background_image = self.extract_background_image_from_poster(image, movie_id)
                except Exception as e:
                    print(f"Warning: Could not extract background image: {e}")
            
            # Create movie object
            if image and title:
                movie = YidioMovie(
                    title=title,
                    image=image,
                    classification=classification,
                    year=year,
                    length=length,
                    imdb_rating=imdb_rating,
                    description=description,
                    background_image=background_image,
                    tagline=tagline,
                    where_to_watch=where_to_watch,
                    genres=genres,
                    cast=cast,
                    director=director,
                    metascore=metascore,
                    mpaa_rating=mpaa_rating
                )
                return movie
            else:
                print(f"Title or image not found in HTML file: {os.path.basename(file_path) if file_path else 'unknown'}")
                return None
                
        except Exception as e:
            print(f"Error processing HTML content: {e}")
            return None

        
    # Funct to save the data in a csv file (For analysis purposes)
    def save_to_csv(self, movies_list):
        if not isinstance(movies_list, list):
            movies_list = [movies_list]

        csv_filename = 'movies.csv'

        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Image', 'Classification', 'Year', 'Length', 'IMDB Rate', 'Description', 
                          'Background Image', 'Tagline', 'Where to Watch', 'Genres', 'Cast', 'Director', 'Metascore', 'MPAA Rating']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for movie in movies_list:
                writer.writerow({
                    'Title': movie.title,
                    'Image': movie.image,
                    'Classification': movie.classification,
                    'Year': movie.year,
                    'Length': movie.length,
                    'IMDB Rate': movie.imdb_rating,
                    'Description': movie.description,
                    'Background Image': movie.background_image,
                    'Tagline': movie.tagline,
                    'Where to Watch': movie.where_to_watch,
                    'Genres': movie.genres,
                    'Cast': movie.cast,
                    'Director': movie.director,
                    'Metascore': movie.metascore,
                    'MPAA Rating': movie.mpaa_rating
                })

