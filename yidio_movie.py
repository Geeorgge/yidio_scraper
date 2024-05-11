
class Movie:
    def __init__(self, image, title, classification, year, length, imdb_rating, description):
        self.image = image
        self.title = title
        self.classification = classification
        self.year = year
        self.length = length
        self.imdb_rating = imdb_rating
        self.description = description


    def __str__(self):
        return f"Title: {self.title}\n" \
               f"Classification: {self.classification}\n" \
               f"Year: {self.year}\n" \
               f"length: {self.length}\n" \
               f"IMDB Rating: {self.imdb_rating}\n" \
               f"Description: {self.description}"
