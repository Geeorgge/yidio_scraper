import React from 'react';
import { Star } from 'lucide-react';

const MovieList = ({ movies }) => {
  if (movies.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <p className="text-gray-500 text-xl">No movies found.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-4">
      {movies.map((movie) => (
        <div
          key={movie.id}
          className="bg-[#2a2a40] text-[#f0f0f0] rounded-xl p-4 shadow-md hover:shadow-lg hover:scale-105 transition-all duration-300">
          {movie.image && (
            <img
              src={movie.image.startsWith('http') ? movie.image : `https:${movie.image}`}
              alt={movie.title}
              className="w-40 h-60 object-cover rounded mb-2"
            />
          )}
          <h2 className="text-sm mb-1 font-bold">
            {movie.title} <span className="text-sm text-gray-50">({movie.year})</span>
          </h2>
          <p className="text-sm text-gray-60 text-center mb-2 line-clamp-3">{movie.description}</p>

          <div className="flex items-center gap-1 text-white-500 mb-3 font-medium">
            <Star size={18} fill="currentColor" className="text-yellow-500" />
            <span className="text-sm font-medium text-green-20">{movie.imdb_rating || 'N/A'}</span>
          </div>

          <button
            onClick={() => alert(`${movie.description}`)}
            className="mt-auto bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded-md text-sm transition"
          >
            See more
          </button>
        </div>
      ))}
    </div>
  );
};

export default MovieList;
