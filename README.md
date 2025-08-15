# 🎬 Yidio Movie Scraper

This project scrapes movie data from [Yidio.com](https://www.yidio.com/) and exposes it through a Django REST API. It also includes a modern React frontend for browsing and filtering the scraped movies with animations and visual polish.

<img width="1366" height="643" alt="Captura de pantalla de 2025-08-15 14-13-35" src="https://github.com/user-attachments/assets/07d6e686-87f3-42e6-9c8d-e67008d7f773" />


---

## 🚀 Features

- ✅ Robust scraper with retry logic, duplicate detection, and support for local HTML parsing
- ✅ MySQL database for persistent movie storage
- ✅ RESTful API built using Django REST Framework
- ✅ React frontend with dynamic filtering and animations using GSAP
- ✅ Dockerized setup for backend, frontend, and database
- ✅ Dark-themed UI with animated spotlight hover effect on movie cards
- ✅ Pagination and search with debounce in frontend
- ✅ Modular and extensible scraping logic

---

## 🧱 Tech Stack

| Layer       | Stack                                 |
|-------------|----------------------------------------|
| **Backend** | Django, Django REST Framework          |
| **Frontend**| React, Tailwind CSS, GSAP              |
| **Database**| MySQL                                  |
| **Scraping**| Python (`requests`, `BeautifulSoup`)   |
| **Containerization** | Docker + Docker Compose       |

---

## 📁 Project Structure

```bash
├── api/
│   ├── yidio_scraper/
│   │   ├── commands/
│   │   │   ├── yidio_scraper.py
│   │   │   ├── yidio_html_scraper.py
│   │   │   └── yidio_get_links.py
│   │   ├── models.py
│   │   ├── views.py
│   └── management/commands/
│       ├── extract_movie_data.py
│       └── extract_movie_data_from_html.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MovieList.jsx
│   │   │   ├── MovieDetail.jsx
│   │   │   └── ChromaGrid.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   └── public/
│       └── index.html
├── docker-compose.yml
└── README.md
```

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/yidio-scraper.git
cd yidio-scraper
```

### 2. Build and run the containers

```bash
docker-compose up --build
```

This will launch:

- Django API at http://localhost:8000
- React frontend at http://localhost:3000
- MySQL database

### 3. Run the scraper manually

```bash
docker-compose exec backend python manage.py extract_movie_data  -->  Parse from Yidio
docker-compose exec backend python manage.py extract_movie_data_from_html  --> Parse from local Html
```

## 📊 Frontend Filters

Users can filter movies by:

- Release year
- Content classification
- IMDb rating

## 📌 Notes

- The scraper is intended for educational/demo purposes and should not be used to overload Yidio's servers.
- All parsing is done in batches and includes retry logic to handle transient errors.
- You can preprocess and clean scraped text before storage or display.
