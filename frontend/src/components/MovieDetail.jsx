import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  Calendar,
  Clock,
  Film,
  Star,
  Ticket,
  ThumbsUp,
  User,
  Users,
  MonitorPlay,
} from "lucide-react";

function MovieDetail() {
  const { id } = useParams(); // Get the movie ID from the route
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch movie data from the backend
    const fetchMovie = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/yidio-movies/${id}/`
        );
        const data = await response.json();
        setMovie(data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching movie details:", error);
        setLoading(false);
      }
    };

    fetchMovie();
  }, [id]);

  const cleanArrayString = (value) => {
    if (!value) return "";
    if (Array.isArray(value)) return value.join(", ");
    // Delete brackets and quotes from string representation of array
    return value.replace(/[\[\]\'"]+/g, "");
  };


  if (loading) {
    return <div className="text-center mt-10 text-lg">Loading...</div>;
  }

  if (!movie) {
    return (
      <div className="text-center mt-10 text-red-500">Movie not found.</div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-4 text-white">
      <Link to="/" className="text-blue-400 hover:underline inline-block mb-6 font-bold">
        ← Back to list
      </Link>

      <div className="bg-gray-900 text-white p-6 rounded-2xl shadow-xl max-w-4xl mx-auto">
        {/* Imagen con hover */}
        {movie.image && (
          <div className="overflow-hidden rounded-xl mb-4 w-48 mx-auto">
            <img
              src={movie.image}
              alt={movie.title}
              className="w-full h-auto object-cover transform transition-transform duration-300 hover:scale-105 shadow-md"
            />
          </div>
        )}

        {/* Título */}
        <h2 className="text-3xl font-bold text-center mb-1">{movie.title}</h2>

        {/* Tagline */}
        {movie.tagline && (
          <p className="text-center text-gray-400 italic text-sm mb-4">
            {movie.tagline}
          </p>
        )}

        {/* Año y duración */}
        <div className="flex justify-center gap-6 text-gray-300 text-sm mb-2">
          <div className="flex items-center gap-1">
            <Calendar size={16} color="#0adc0dff"/>
            <span>{movie.year}</span>
          </div>
          <div className="flex items-center gap-1">
            <Clock size={16} color="#ffffffff"/>
            <span>{movie.length}</span>
          </div>
        </div>

        {/* Clasificación, IMDB, MPAA, Metascore */}
        <div className="flex flex-wrap justify-center gap-6 text-gray-300 text-sm mb-4">
          <div className="flex items-center gap-1">
            <Ticket size={16} color="#d20b0bff"/>
            <span>{movie.classification}</span>
          </div>
          <div className="flex items-center gap-1">
            <Star size={16} color="#facc15"/>
            <span>{movie.imdb_rating}</span>
          </div>
          <div className="flex items-center gap-1">
            <ThumbsUp size={16} color="#60a5fa"/>
            <span>{movie.mpaa_rating}</span>
          </div>
          <div className="flex items-center gap-1">
            <Film size={16} color="#ffffffff"/>
            <span>{movie.metascore}</span>
          </div>
        </div>

        {/* Géneros */}
        {movie.genres && (
          <p className="text-sm text-gray-200 mb-1">
            <strong>Genres:</strong>{" "}
             {cleanArrayString(movie.genres)}.
          </p>
        )}

        {/* Cast */}
        {movie.cast && (
          <p className="text-sm text-gray-200 mb-1">
            <strong>Cast:</strong>{" "}
            {cleanArrayString(movie.cast)}.
          </p>
        )}

        {/* Director */}
        {movie.director && (
          <p className="text-sm text-gray-200 mb-1">
            <strong>Director:</strong>{" "}
            {cleanArrayString(movie.director)}.
          </p>
        )}

        {/* Where to watch */}
        {movie.where_to_watch && (
          <p className="text-sm text-gray-200 mb-2">
            <MonitorPlay size={14} className="inline mr-1" />
            <strong>Available On:</strong> {movie.where_to_watch}
          </p>
        )}

        {/* Descripción */}
        <p className="text-sm text-gray-100 leading-relaxed mt-2">
        <strong>Description:</strong>
          <p>
            {movie.description}
          </p>
        </p>
      </div>
    </div>
  );
}
export default MovieDetail;
