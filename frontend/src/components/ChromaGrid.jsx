import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { Link } from "react-router-dom";
import "./ChromaGrid.css";

const ChromaGrid = ({ movies = [] }) => {
  const rootRef = useRef(null);
  const fadeRef = useRef(null);
  const setX = useRef(null);
  const setY = useRef(null);
  const pos = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const el = rootRef.current;
    if (!el) return;
    setX.current = gsap.quickSetter(el, "--x", "px");
    setY.current = gsap.quickSetter(el, "--y", "px");
    const { width, height } = el.getBoundingClientRect();
    pos.current = { x: width / 2, y: height / 2 };
    setX.current(pos.current.x);
    setY.current(pos.current.y);
  }, []);

  const moveTo = (x, y) => {
    gsap.to(pos.current, {
      x,
      y,
      duration: 0.45,
      ease: "power3.out",
      onUpdate: () => {
        setX.current?.(pos.current.x);
        setY.current?.(pos.current.y);
      },
      overwrite: true,
    });
  };

  const handleMove = (e) => {
    const gridRect = rootRef.current.getBoundingClientRect();
    const x = e.clientX - gridRect.left;
    const y = e.clientY - gridRect.top;

    const radius = 300; // must match --r in CSS
    const cards = rootRef.current.querySelectorAll(".chroma-card");

    cards.forEach((card) => {
      const rect = card.getBoundingClientRect();
      const cx = rect.left + rect.width / 2 - gridRect.left;
      const cy = rect.top + rect.height / 2 - gridRect.top;
      const dist = Math.hypot(x - cx, y - cy);

      if (dist < radius) {
        card.setAttribute("data-active", "true");
      } else {
        card.removeAttribute("data-active");
      }
    });
  };

  const handleLeave = () => {
    const cards = rootRef.current.querySelectorAll(".chroma-card");
    cards.forEach((card) => card.removeAttribute("data-active"));
  };

  const handleCardMove = (e) => {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.setProperty("--mouse-x", `${x}px`);
    card.style.setProperty("--mouse-y", `${y}px`);
  };

  return (
    <div
      ref={rootRef}
      className="chroma-grid"
      onPointerMove={handleMove}
      onPointerLeave={handleLeave}
    >
      {movies.map((movie) => (
        <Link to={`/movies/${movie.id}`} key={movie.id}>
          <article
            className="chroma-card"
            onMouseMove={handleCardMove}
            style={{
              "--card-border": "#3b82f6",
              "--card-gradient": "linear-gradient(145deg,#0f172a,#1e293b)",
            }}
          >
            <div className="chroma-img-wrapper">
              <img
                src={
                  movie.image?.startsWith("http")
                    ? movie.image
                    : `https:${movie.image}`
                }
                alt={movie.title}
              />
            </div>
            <footer className="chroma-info">
              <h3 className="name">{movie.title}</h3>
              <p className="role">{movie.year}</p>
            </footer>
          </article>
        </Link>
      ))}
      <div className="chroma-light" />
    </div>
  );
};

export default ChromaGrid;
