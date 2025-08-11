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
            
            # Convert lists to comma-separated strings
            genres =    ", ".join(movie.genres)   if isinstance(movie.genres, list)   else movie.genres
            cast =      ", ".join(movie.cast)     if isinstance(movie.cast, list)     else movie.cast
            director =  ", ".join(movie.director) if isinstance(movie.director, list) else movie.director

            insert_query = """
            INSERT INTO yidio_scraper_movie (
                title, image, background_image, tagline,
                classification, mpaa_rating, year, length,
                imdb_rating, metascore, description,
                genres, cast, director, where_to_watch
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                mpaa_rating = VALUES(mpaa_rating),
                metascore = VALUES(metascore)
            """
            movie_data = (
                movie.title,
                movie.image,
                movie.background_image,
                movie.tagline,
                movie.classification,
                movie.mpaa_rating,
                movie.year,
                movie.length,
                movie.imdb_rating,
                movie.metascore,
                movie.description,
                genres,
                cast,
                director,
                movie.where_to_watch
            )

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