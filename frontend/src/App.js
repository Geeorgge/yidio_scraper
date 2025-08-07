import React, { useState, useEffect } from "react";
import MovieList from "./components/MovieList";
import "./App.css";

function App() {
  const [movies, setMovies] = useState([]); // Movies state
  const [page, setPage] = useState(1); // Current page
  const [totalMovies, setTotalMovies] = useState(0); // Total movies from API
  const [searchTerm, setSearchTerm] = useState(""); // Search term state
  const [debouncedSearch, setDebouncedSearch] = useState("");  // Debounced search term
  const [loading, setLoading] = useState(false); // Loading state
  const limit = 12; // Pages per page

  // Debounce effect (waits 500ms before updating the search term)
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(searchTerm);
    }, 500);

    return () => {
      clearTimeout(handler);
    };
  }, [searchTerm]);

  useEffect(() => {
    const offset = (page - 1) * limit;
    const searchParam = debouncedSearch ? `&search=${encodeURIComponent(debouncedSearch)}` : '';
    const url = `http://localhost:8000/api/yidio-movies/?limit=${limit}&offset=${offset}${searchParam}`;

    setLoading(true);
    console.log("Fetching:", url);
    fetch(url)
      .then(res => res.json())
      .then(data => {
        console.log("Fetched data:", data);
        setMovies(data.results || []);
        setTotalMovies(data.count || 0);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching movies:", err);
        setLoading(false);
      });
  }, [page, debouncedSearch]);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
    setPage(1); // Reset to first page on search
  };

  const totalPages = Math.ceil(totalMovies / limit);

  return (
    <div className="min-h-screen text-white bg-gradient-to-r from-gray-900 via-gray-800 to-black p-8">
      <h1 className="text-4xl font-bold mb-6 text-center">🎬 Movie Explorer</h1>

      <div className="flex justify-center mb-6">
        <input
          type="text"
          placeholder="Search by title..."
          value={searchTerm}
          onChange={handleSearchChange}
          className="px-4 py-2 rounded w-96 text-black"
        />
      </div>

      {loading ? (
        <p className="text-center">Loadin movies...</p>
      ) : (
        <MovieList movies={movies} />
      )}

      {!loading && movies.length > 0 && (
        <div className="flex justify-center mt-6 gap-4">
          <button
            onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
            disabled={page === 1}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded disabled:opacity-50"
          >
            Prev
          </button>
          <span className="self-center">Page {page} of {totalPages}</span>
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
