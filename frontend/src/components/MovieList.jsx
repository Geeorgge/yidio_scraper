import React from "react";
import ChromaGrid from "./ChromaGrid";

const MovieList = ({ movies }) => {
  if (!movies || movies.length === 0) {
    return <p className="text-center text-gray-400 text-lg">No movies found.</p>;
  }

  return <ChromaGrid movies={movies} />;
};

export default MovieList;
