import re
import csv
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from yidio_scraper.models import YidioMovie
from selenium.webdriver.chrome.options import Options

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


    # Function to get dynamic fields using Selenium
    def get_dynamic_fields(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            options=chrome_options
        )

        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # MPAA Rating y Metascore
        mpaa_rating, metascore = None, None
        attributes = soup.select("ul.attributes li")
        for li in attributes:
            name_div = li.select_one("div.name")
            value_div = li.select_one("div.value")
            if name_div and value_div:
                label = name_div.get_text(strip=True).lower()
                value = value_div.get_text(strip=True)
                if "mpaa rating" in label:
                    mpaa_rating = value
                elif "metascore" in label:
                    metascore = value

        driver.quit()
        return mpaa_rating, metascore

    # Process the movie attrs to crate objects
    def get_movie_info(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            image =             self.extract_image(soup)
            title =             self.extract_title(soup)
            classification =    self.extract_classification(soup)
            year =              self.extract_year(soup)
            length =            self.extract_length(soup)
            imdb_rating =       self.extract_imdb_rating(soup)
            description =       self.extract_description(soup)
            tagline =           self.extract_tagline(soup)
            where_to_watch =    self.extract_where_to_watch(soup)
            genres =            self.extract_genres(soup)
            cast =              self.extract_cast(soup)
            director =          self.extract_director(soup)

            # Fields via Selenium 
            mpaa_rating, metascore = self.get_dynamic_fields(url)

            match = re.search(r'/movie/.+?/(\d+)', url) # Extract movie ID from URL
            movie_id = match.group(1) if match else None # Get movie ID or None

            # Extract background image from poster
            background_image = self.extract_background_image_from_poster(image, movie_id)
    
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
                print("Title or image not found")
                return None
        else:
            print("Error fetching the page:", response.status_code)
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

