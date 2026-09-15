from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert data["endpoints"]["random_movie"] == "/movie/random"
    assert data["endpoints"]["genre_movie"] == "/movie/genre/{genre}"


def test_random_movie():
    response = client.get("/movie/random")
    assert response.status_code == 200
    data = response.json()
    assert "movie" in data
    assert "message" in data
    movie = data["movie"]
    assert "id" in movie
    assert "title" in movie
    assert "year" in movie
    assert "director" in movie
    assert "cast" in movie
    assert "genres" in movie
    assert "language" in movie
    assert "duration_minutes" in movie
    assert "rating" in movie
    assert "synopsis" in movie
    assert "streaming_platforms" in movie
    assert isinstance(movie["cast"], list)
    assert isinstance(movie["genres"], list)
    assert isinstance(movie["streaming_platforms"], list)
    assert len(movie["title"]) > 0
    assert movie["year"] > 1900
    assert 0 <= movie["rating"] <= 10


def test_random_movie_with_genre_filter():
    response = client.get("/movie/random?genre=Action")
    assert response.status_code == 200
    data = response.json()
    movie = data["movie"]
    assert "Action" in movie["genres"]


def test_random_movie_with_language_filter():
    response = client.get("/movie/random?language=Hindi")
    assert response.status_code == 200
    data = response.json()
    movie = data["movie"]
    assert movie["language"] == "Hindi"


def test_random_movie_with_both_filters():
    response = client.get("/movie/random?genre=Romance&language=English")
    assert response.status_code == 200
    data = response.json()
    movie = data["movie"]
    assert "Romance" in movie["genres"]
    assert movie["language"] == "English"


def test_random_movie_no_match():
    response = client.get("/movie/random?genre=NonExistentGenre")
    assert response.status_code == 404


def test_genre_movie():
    response = client.get("/movie/genre/Comedy")
    assert response.status_code == 200
    data = response.json()
    assert "movie" in data
    assert "message" in data
    movie = data["movie"]
    assert "Comedy" in movie["genres"]
    assert data["message"] == "Here's a Comedy movie for you!"


def test_genre_movie_with_language_filter():
    response = client.get("/movie/genre/Comedy?language=Hindi")
    assert response.status_code == 200
    data = response.json()
    movie = data["movie"]
    assert "Comedy" in movie["genres"]
    assert movie["language"] == "Hindi"


def test_genre_movie_not_found():
    response = client.get("/movie/genre/NonExistent")
    assert response.status_code == 404


def test_available_genres():
    response = client.get("/genres")
    assert response.status_code == 200
    data = response.json()
    assert "genres" in data
    assert "count" in data
    assert isinstance(data["genres"], list)
    assert data["count"] == len(data["genres"])
    assert data["count"] >= 6
    assert "Action" in data["genres"]
    assert "Comedy" in data["genres"]
    assert "Drama" in data["genres"]
    assert "Thriller" in data["genres"]
    assert "Sci-Fi" in data["genres"]
    assert "Romance" in data["genres"]


def test_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_movies" in data
    assert "genres" in data
    assert "languages" in data
    assert data["total_movies"] >= 70
    assert isinstance(data["genres"], dict)
    assert isinstance(data["languages"], dict)
    assert sum(data["genres"].values()) >= data["total_movies"]
    assert "English" in data["languages"]
    assert "Hindi" in data["languages"]


def test_movie_schema_consistency():
    response = client.get("/movie/random")
    movie = response.json()["movie"]
    for platform in movie["streaming_platforms"]:
        assert "name" in platform
        assert len(platform["name"]) > 0
    for actor in movie["cast"]:
        assert len(actor) > 0
    for genre in movie["genres"]:
        assert len(genre) > 0
    assert movie["duration_minutes"] > 0
