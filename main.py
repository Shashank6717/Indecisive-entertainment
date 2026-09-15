import random
import json
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from database import get_db, init_db, MovieDB
from models import (
    Movie,
    RandomMovieResponse,
    GenreMovieResponse,
    AvailableGenresResponse,
    StatsResponse,
    StreamingPlatform,
)
from seed import seed_database

app = FastAPI(
    title="Movie Pick API",
    description="Can't decide what to watch? Let us pick for you! A movie recommendation API with a curated corpus of films across genres and languages.",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    init_db()
    seed_database()


def db_movie_to_movie(db_movie: MovieDB) -> Movie:
    return Movie(
        id=db_movie.id,
        title=db_movie.title,
        year=db_movie.year,
        director=db_movie.director,
        cast=db_movie.cast.split(","),
        genres=[g.strip() for g in db_movie.genres.split(",")],
        language=db_movie.language,
        duration_minutes=db_movie.duration_minutes,
        rating=db_movie.rating,
        synopsis=db_movie.synopsis,
        streaming_platforms=[
            StreamingPlatform(name=p.strip())
            for p in db_movie.streaming_platforms.split(",")
        ],
        poster_url=db_movie.poster_url,
    )


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the Movie Pick API! 🎬",
        "docs": "/docs",
        "endpoints": {
            "random_movie": "/movie/random",
            "genre_movie": "/movie/genre/{genre}",
            "all_genres": "/genres",
            "stats": "/stats",
        },
    }


@app.get("/movie/random", response_model=RandomMovieResponse, tags=["Movies"])
def get_random_movie(
    genre: Optional[str] = Query(
        None, description="Optional genre filter (e.g., Action, Comedy)"
    ),
    language: Optional[str] = Query(
        None, description="Optional language filter (e.g., English, Hindi)"
    ),
    db: Session = Depends(get_db),
):
    query = db.query(MovieDB)

    if genre:
        query = query.filter(MovieDB.genres.ilike(f"%{genre}%"))
    if language:
        query = query.filter(MovieDB.language.ilike(f"%{language}%"))

    count = query.count()
    if count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No movies found matching your criteria (genre={genre}, language={language})",
        )

    offset = random.randint(0, count - 1)
    db_movie = query.offset(offset).first()

    return RandomMovieResponse(
        movie=db_movie_to_movie(db_movie),
        message="Can't decide? Here's a random pick for you!",
    )


@app.get(
    "/movie/genre/{genre}",
    response_model=GenreMovieResponse,
    tags=["Movies"],
)
def get_movie_by_genre(
    genre: str,
    language: Optional[str] = Query(
        None, description="Optional language filter"
    ),
    db: Session = Depends(get_db),
):
    query = db.query(MovieDB).filter(MovieDB.genres.ilike(f"%{genre}%"))

    if language:
        query = query.filter(MovieDB.language.ilike(f"%{language}%"))

    count = query.count()
    if count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No movies found in genre '{genre}'"
            + (f" with language '{language}'" if language else ""),
        )

    offset = random.randint(0, count - 1)
    db_movie = query.offset(offset).first()

    return GenreMovieResponse(
        movie=db_movie_to_movie(db_movie),
        message=f"Here's a {genre} movie for you!",
    )


@app.get("/genres", response_model=AvailableGenresResponse, tags=["Metadata"])
def get_available_genres(db: Session = Depends(get_db)):
    all_genres_raw = db.query(MovieDB.genres).all()
    genre_set = set()
    for (genres_str,) in all_genres_raw:
        for g in genres_str.split(","):
            genre_set.add(g.strip())

    sorted_genres = sorted(genre_set)
    return AvailableGenresResponse(genres=sorted_genres, count=len(sorted_genres))


@app.get("/stats", response_model=StatsResponse, tags=["Metadata"])
def get_stats(db: Session = Depends(get_db)):
    total = db.query(MovieDB).count()

    all_genres_raw = db.query(MovieDB.genres).all()
    genre_counts = {}
    for (genres_str,) in all_genres_raw:
        for g in genres_str.split(","):
            g = g.strip()
            genre_counts[g] = genre_counts.get(g, 0) + 1

    all_languages = db.query(MovieDB.language).all()
    lang_counts = {}
    for (lang,) in all_languages:
        lang_counts[lang] = lang_counts.get(lang, 0) + 1

    return StatsResponse(
        total_movies=total, genres=genre_counts, languages=lang_counts
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
