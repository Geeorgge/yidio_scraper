import re
import requests
from bs4 import BeautifulSoup
from yidio_movie import Movie

def extract_image(soup):
    content_div = soup.find('div', class_='content')
    if content_div:
        image_src = content_div.select_one('div[class="poster movie"] img')['src'].strip()
        return image_src
    return None

def extract_title(soup):
    content_div = soup.find('div', class_='content')
    if content_div:
        title_elem = content_div.select_one('div.details h1')
        if title_elem:
            title = title_elem.text.strip().replace('Watch ', '')
            return title
        
    return None

def extract_imdb_rating(soup):
    imdb_rating_div = soup.select_one('ul.attributes > li.imdb')
    if imdb_rating_div:
        imdb_rating_span = imdb_rating_div.select_one('span')
        if imdb_rating_span:
            imdb_rating_span.decompose()
        imdb_rating = imdb_rating_div.text.strip()
        return imdb_rating
    return None

def extract_year(soup):
    year_elem = soup.select_one('ul.attributes > li:nth-of-type(2)')
    if year_elem:
        year = year_elem.text.strip()
        return year
    return None

def extract_length(soup):
    length_elem = soup.select_one('ul.attributes > li:nth-of-type(3)')
    if length_elem:
        length = length_elem.text.strip()
        return length
    return None

def extract_classification(soup):
    classification_elem = soup.select_one('ul.attributes > li:nth-of-type(1)')
    if classification_elem:
        classification = classification_elem.text.strip()
        allowed_classifications = ["R", "PG-13", "PG", "G", "NC-17", "NR"]
        if classification not in allowed_classifications:
            classification = None
        return classification
    return None

def extract_description(soup):
    description_elem = soup.select_one('div.description p')
    if description_elem:
        description_text = description_elem.text.strip()
        description_text = re.sub(r'[^ -~]', '', description_text)
        try:
            description = description_text.encode('utf-8').decode('utf-8')
            return description
        except UnicodeEncodeError as e:
            print("Error de codificación:", e)
    return None

def get_movie_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        image = extract_image(soup)
        title = extract_title(soup)
        imdb_rating = extract_imdb_rating(soup)
        year = extract_year(soup)
        length = extract_length(soup)
        classification = extract_classification(soup)
        description = extract_description(soup)
        
        if image and title:
            movie = Movie(image, title, classification, year, length, imdb_rating, description)
            return movie
        else:
            print("Title or image not found")
            return None
    else:
        print("Error fetching the page:", response.status_code)
        return None

if __name__ == "__main__":
    movies_list = []

    with open("links.txt", "r") as file:
        movie_links = file.readlines()
    for link in movie_links:
        link = link.strip()
        movie_info = get_movie_info(link)
        if movie_info:
            movies_list.append(movie_info)

    for movie in movies_list:
        movie_data = {
            'Title': movie.title,
            'Image': movie.image,
            'Classification': movie.classification,
            'Year': movie.year,
            'length': movie.length,
            'IMDB Rate': movie.imdb_rating,
            'Description': movie.description
        }