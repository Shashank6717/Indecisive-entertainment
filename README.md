# Indecisive Entertainment

> Can't decide what to watch? Let the API decide for you.

A FastAPI-powered movie recommendation server backed by SQLite. It serves random movies or genre-filtered picks from a curated corpus of 70 films across multiple languages and genres.

---

## Why This Exists

We've all been there — scrolling through streaming platforms for 45 minutes, only to rewatch something we've already seen. The paradox of choice kills decision-making. This API removes the decision burden entirely:

- **You're feeling indecisive?** Hit the random endpoint. You get one movie. Watch it.
- **You know the genre but not the movie?** Pick a genre, get a random film from that genre.

No ratings algorithm, no collaborative filtering, no over-engineered recommendation system. Just a curated corpus and a random number generator. Simple works.

---

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Framework | FastAPI | Async-ready, automatic docs, type-safe |
| Database | SQLite via SQLAlchemy | Zero config, portable, file-based |
| Validation | Pydantic v2 | FastAPI's native validation layer |
| Server | Uvicorn | Lightweight ASGI server |

---

## Project Structure

```
movie-pick/
├── main.py          # FastAPI app and route definitions
├── database.py      # SQLAlchemy engine, session, and ORM model
├── models.py        # Pydantic schemas for request/response validation
├── seed.py          # Movie corpus data and database seeder
├── requirements.txt # Python dependencies
├── movies.db        # SQLite database (created on first run)
└── README.md
```

---

## Setup & Run

```bash
# 1. Clone or download the project
cd movie-pick

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the server
python main.py
```

The server starts at `http://localhost:8000`. The database is created and seeded automatically on first run.

Interactive API docs available at `http://localhost:8000/docs`.

### Docker

```bash
# Build the image
docker build -t movie-pick .

# Run the container
docker run -d -p 8000:8000 --name movie-pick movie-pick

# Stop and remove
docker stop movie-pick && docker rm movie-pick
```

---

## API Endpoints

### `GET /` — Welcome

Returns available endpoints.

### `GET /movie/random` — Random Movie Pick

Returns a random movie from the entire corpus.

**Query Parameters (optional):**

| Param | Type | Description |
|-------|------|-------------|
| `genre` | string | Filter by genre (e.g., `Action`, `Comedy`) |
| `language` | string | Filter by language (e.g., `English`, `Hindi`) |

**Examples:**
```
GET /movie/random
GET /movie/random?genre=Thriller
GET /movie/random?language=Korean
GET /movie/random?genre=Sci-Fi&language=English
```

**Response:**
```json
{
  "movie": {
    "id": 1,
    "title": "The Dark Knight",
    "year": 2008,
    "director": "Christopher Nolan",
    "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
    "genres": ["Action", "Thriller"],
    "language": "English",
    "duration_minutes": 152,
    "rating": 9.0,
    "synopsis": "When the menace known as the Joker wreaks havoc on Gotham...",
    "streaming_platforms": [
      {"name": "Netflix", "url": null},
      {"name": "HBO Max", "url": null},
      {"name": "Amazon Prime", "url": null}
    ],
    "poster_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911M5nRQYqFGqLi.jpg"
  },
  "message": "Can't decide? Here's a random pick for you!"
}
```

### `GET /movie/genre/{genre}` — Movie by Genre

Returns a random movie from the specified genre.

**Path Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `genre` | string | Genre name (e.g., `Action`, `Romance`) |

**Query Parameters (optional):**

| Param | Type | Description |
|-------|------|-------------|
| `language` | string | Filter by language |

**Examples:**
```
GET /movie/genre/Comedy
GET /movie/genre/Drama?language=Hindi
GET /movie/genre/Sci-Fi
```

### `GET /genres` — List All Genres

Returns all available genres and their count.

**Response:**
```json
{
  "genres": ["Action", "Comedy", "Drama", "Romance", "Sci-Fi", "Thriller"],
  "count": 6
}
```

### `GET /stats` — Corpus Statistics

Returns total movie count, genre distribution, and language distribution.

**Response:**
```json
{
  "total_movies": 70,
  "genres": {
    "Action": 12,
    "Comedy": 12,
    "Drama": 12,
    "Romance": 12,
    "Sci-Fi": 10,
    "Thriller": 12
  },
  "languages": {
    "English": 35,
    "Hindi": 14,
    "Korean": 4,
    "Telugu": 2,
    "Tamil": 2,
    "Cantonese": 1,
    "Kannada": 1,
    "Indonesian": 1,
    "Malayalam": 1
  }
}
```

---

## Corpus Overview

70 movies across **6 genres** and **9 languages**:

| Genre | Count | Sample Languages |
|-------|-------|-----------------|
| Action | 12 | English, Telugu, Kannada, Indonesian, Cantonese |
| Comedy | 12 | English, Hindi, Korean |
| Drama | 12 | English, Hindi, Korean, Malayalam |
| Thriller | 12 | English, Hindi, Korean |
| Sci-Fi | 10 | English, Tamil |
| Romance | 12 | English, Hindi, Korean, Tamil |

Each movie includes:
- Title, year, director, cast
- Genres (multi-tag)
- Language
- Duration (minutes)
- IMDB rating
- Synopsis
- Streaming platform availability
- Poster URL (TMDB)

---

## Data Schema

```
Movie
├── id: int
├── title: str
├── year: int
├── director: str
├── cast: List[str]
├── genres: List[str]
├── language: str
├── duration_minutes: int
├── rating: float (IMDB out of 10)
├── synopsis: str
├── streaming_platforms: List[StreamingPlatform]
│   ├── name: str
│   └── url: Optional[str]
└── poster_url: Optional[str]
```

---

## License

MIT
