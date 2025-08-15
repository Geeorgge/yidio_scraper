import React, { useState, useEffect } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import MovieList from "./components/MovieList";
import MovieDetail from "./components/MovieDetail";
import "./App.css";

function App() {
  const [movies, setMovies] = useState([]);
  const [page, setPage] = useState(1);
  const [totalMovies, setTotalMovies] = useState(0);
  const [searchTerm, setSearchTerm] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const limit = 35;

  const location = useLocation();
  const isMovieList = location.pathname === "/";

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(searchTerm);
    }, 500);
    return () => clearTimeout(handler);
  }, [searchTerm]);

  useEffect(() => {
    const offset = (page - 1) * limit;
    const searchParam = debouncedSearch
      ? `&search=${encodeURIComponent(debouncedSearch)}`
      : "";
    const url = `http://localhost:8000/api/yidio-movies/?limit=${limit}&offset=${offset}${searchParam}`;

    setLoading(true);
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setMovies(data.results || []);
        setTotalMovies(data.count || 0);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching movies:", err);
        setLoading(false);
      });
  }, [page, debouncedSearch]);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
    setPage(1);
  };

  const totalPages = Math.ceil(totalMovies / limit);

  return (
    <div
      className="min-h-screen text-white to-black px-4 py-8"
      style={{
        background: "linear-gradient(to right, #0f0c29, #302b63, #24243e",
      }}
    >
      <h1 className="text-4xl font-bold mb-6 text-center">🎬 Movie Explorer</h1>

      {isMovieList && (
        <div className="flex justify-center mb-6">
          <input
            type="text"
            placeholder="Search by title..."
            value={searchTerm}
            onChange={handleSearchChange}
            className="px-4 py-2 rounded w-96 text-black"
          />
        </div>
      )}

      {loading ? (
        <p className="text-center">Loading movies...</p>
      ) : (
        <Routes>
          <Route path="/" element={<MovieList movies={movies} />} />
          <Route path="/movies/:id" element={<MovieDetail />} />
        </Routes>
      )}

      {isMovieList && !loading && movies.length > 0 && (
        <div className="flex justify-center mt-6 gap-4">
          <button
            onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
            disabled={page === 1}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded disabled:opacity-50"
          >
            Prev
          </button>
          <span className="self-center">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
            disabled={page === totalPages}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
