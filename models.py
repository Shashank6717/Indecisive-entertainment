from pydantic import BaseModel, Field
from typing import List, Optional


class StreamingPlatform(BaseModel):
    name: str = Field(..., example="Netflix")
    url: Optional[str] = Field(None, example="https://netflix.com/title/12345")


class Movie(BaseModel):
    id: int = Field(..., example=1)
    title: str = Field(..., example="Inception")
    year: int = Field(..., example=2010)
    director: str = Field(..., example="Christopher Nolan")
    cast: List[str] = Field(..., example=["Leonardo DiCaprio", "Joseph Gordon-Levitt"])
    genres: List[str] = Field(..., example=["Sci-Fi", "Action"])
    language: str = Field(..., example="English")
    duration_minutes: int = Field(..., example=148)
    rating: float = Field(..., example=8.8, description="IMDB rating out of 10")
    synopsis: str = Field(
        ...,
        example="A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
    )
    streaming_platforms: List[StreamingPlatform] = Field(
        ..., example=[StreamingPlatform(name="Netflix")]
    )
    poster_url: Optional[str] = Field(
        None, example="https://image.tmdb.org/t/p/w500/9gkRadz0W9S23Z6dRfNoe0E3rz.jpg"
    )


class MovieResponse(BaseModel):
    movie: Movie
    message: str = Field(
        ..., example="Here's a movie for you to watch!"
    )


class GenreMovieRequest(BaseModel):
    genre: str = Field(
        ...,
        example="Sci-Fi",
        description="Genre to filter movies by",
    )


class RandomMovieResponse(BaseModel):
    movie: Movie
    message: str = Field(
        ..., example="Can't decide? Here's a random pick for you!"
    )


class GenreMovieResponse(BaseModel):
    movie: Movie
    message: str = Field(
        ..., example="Here's a Sci-Fi movie for you!"
    )


class AvailableGenresResponse(BaseModel):
    genres: List[str]
    count: int


class StatsResponse(BaseModel):
    total_movies: int
    genres: dict
    languages: dict
