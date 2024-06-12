import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
      axios.get('http://localhost:8000/yidio_scraper/')
          .then(response => {
              setMovies(response.data);
          })
          .catch(error => {
              console.error("There was an error fetching the movies!", error);
          });
  }, []);

  return (
      <div className="App">
          <h1>Movies</h1>
          <ul>
          {movies.map(movie => (
                    <li key={movie.id}>
                        <h2>{movie.title}</h2>
                        <img src={movie.image} alt={movie.title} />
                        <p>{movie.description}</p>
                        <p><strong>Classification:</strong> {movie.classification}</p>
                        <p><strong>Year:</strong> {movie.year}</p>
                        <p><strong>Length:</strong> {movie.length}</p>
                        <p><strong>IMDB Rating:</strong> {movie.imdb_rating}</p>
                    </li>
                ))}
          </ul>
      </div>
  );
}

export default App;
