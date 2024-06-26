import re
import csv
import requests
from bs4 import BeautifulSoup
from yidio_scraper.models import Movie

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

    # Funct to extract the title movie
    def extract_title(self, soup):
        content_div = soup.find('div', class_='content')
        if content_div:
            title_elem = content_div.select_one('div.details h1')
            if title_elem:
                title = title_elem.text.strip().replace('Watch ', '')
                return title
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
        year_elem = soup.select_one('ul.attributes > li:nth-of-type(2)')
        if year_elem:
            year = year_elem.text.strip()
            if year.isdigit() and len(year) == 4:
                return year
            year_elem = soup.select_one('ul.attributes > li:nth-of-type(1)')
            year = year_elem.text.strip()
            return year

        return 'Unknown'  

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

    # Process the movie attrs to crate objects
    def get_movie_info(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            image = self.extract_image(soup)
            title = self.extract_title(soup)
            classification = self.extract_classification(soup)
            year = self.extract_year(soup)
            length = self.extract_length(soup)
            imdb_rating = self.extract_imdb_rating(soup)
            description = self.extract_description(soup)
            
            if image and title:
                movie = Movie(
                    title=title,
                    image=image,
                    classification=classification,
                    year=year,
                    length=length,
                    imdb_rating=imdb_rating,
                    description=description
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
            fieldnames = ['Title', 'Image', 'Classification', 'Year', 'Length', 'IMDB Rate', 'Description']

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
                    'Description': movie.description
                })

        print(f"Data saved in {csv_filename}")
