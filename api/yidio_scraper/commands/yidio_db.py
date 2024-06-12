import mysql.connector

def save_to_database(movies_list):

    if not isinstance(movies_list, list):
        movies_list = [movies_list]

    connection = mysql.connector.connect(
        # Add your mysql user data
        host="",
        user="",
        password="",
        database=""
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