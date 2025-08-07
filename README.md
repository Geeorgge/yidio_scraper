# 🎬 Yidio Movie Scraper

This project scrapes movie data from Yidio.com and exposes it through a Django REST API. It also includes a React frontend for browsing and filtering the scraped movies.

## 🚀 Features

- Robust scraper with error handling and duplicate detection
- MySQL database for persistent storage
- RESTful API built with Django REST Framework
- React frontend with filters (year, classification, IMDb rating)
- Modular scraping and data-saving logic
- Dockerized environment for easy setup

## 🧱 Tech Stack

- **Backend**: Django + Django REST Framework
- **Frontend**: React
- **Database**: MySQL
- **Scraping**: Python (requests + custom HTML parsing)
- **Containerization**: Docker + Docker Compose

## 📁 Project Structure

```
├── backend/
│   ├── yidio_scraper/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── commands/
│   │   │   ├── yidio_scraper.py
│   │   │   ├── yidio_get_links.py
│   ├── api/
│       └── management/commands/
│           └── extract_movie_data.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
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

- Django API at `http://localhost:8000`
- React frontend at `http://localhost:3000`
- MySQL database

### 3. Run the scraper manually

```bash
docker-compose exec backend python manage.py extract_movie_data
```

## 🧹 Duplicate Detection

The model uses a `unique_together` constraint on the fields `title`, `year`, and `length` to avoid duplicates. Additionally, the scraper checks for existing entries before attempting to save new records.

## 📊 Frontend Filters

Users can filter movies by:

- Release year
- Content classification
- IMDb rating

## 📌 Notes

- The scraper is intended for educational/demo purposes and should not be used to overload Yidio's servers.
- All parsing is done in batches and includes retry logic to handle transient errors.
- You can preprocess and clean scraped text before storage or display.

