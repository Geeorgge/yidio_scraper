// src/components/MovieList.jsx
import React from 'react';

const MovieList = ({ movies }) => {
  return (
    <div>
      {movies.length === 0 && <p>No movies found.</p>}
      {movies.map(movie => (
        <div key={movie.id} style={{ marginBottom: '1rem' }}>
          <h2>{movie.title} ({movie.year})</h2>
          {movie.image && <img  src={movie.image.startsWith('http') ? movie.image : `https:${movie.image}`} // ✅ AQUÍ VA
  alt={movie.title}
  style={{ width: '180px', height: '270px' }} />}
          <p>{movie.description}</p>
          <p><b>Rating:</b> {movie.imdb_rating || 'N/A'}</p>
        </div>
      ))}
    </div>
  );
};

export default MovieList;
