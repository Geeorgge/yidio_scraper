import mysql.connector
from yidio_movie_data import get_movie_info, save_to_csv

def save_to_database(movies_list):

    connection = mysql.connector.connect(
        host="",
        user="",
        password="",
        database="yidio_cinema"
    )

    if connection.is_connected():

        for movie in movies_list:
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO movies (title, image, classification, year, length, imdb_rating, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            movie_data = (movie.title, movie.image, movie.classification, movie.year, movie.length, movie.imdb_rating, movie.description)

            try:
                cursor.execute(insert_query, movie_data)
                connection.commit()
                print("Data saved successfully in the DB.")
            except mysql.connector.Error as error:
                print("Error saving the data:", error)
            finally:
                cursor.close()

        connection.close()
        print("DB Conection is closed.")

if __name__ == "__main__":

    movies_list = []

    with open("links.txt", "r") as file:
        movie_links = file.readlines()
    for link in movie_links:
        link = link.strip()
        movie_info = get_movie_info(link)
        if movie_info:
            movies_list.append(movie_info)

    save_to_database(movies_list)
    save_to_csv(movies_list)
