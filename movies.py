from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

# Define data model for movie
class Movie(BaseModel):
    title: str
    director: str
    genre: str

app = FastAPI()

# Movies data
MOVIES = [
    {'title': 'The Shawshank Redemption', 'director': 'Frank Darabont', 'genre': 'drama'},
    {'title': 'The Godfather', 'director': 'Francis Ford Coppola', 'genre': 'crime'},
    {'title': 'Pulp Fiction', 'director': 'Quentin Tarantino', 'genre': 'crime'},
    {'title': 'The Dark Knight', 'director': 'Christopher Nolan', 'genre': 'action'},
    {'title': 'Forrest Gump', 'director': 'Robert Zemeckis', 'genre': 'drama'},
    {'title': 'Inception', 'director': 'Christopher Nolan', 'genre': 'action'},
    {'title': 'The Matrix', 'director': 'Lana and Lilly Wachowski', 'genre': 'action'},
    {'title': "Schindler's List", 'director': 'Steven Spielberg', 'genre': 'biography'},
    {'title': 'The Lord of the Rings: The Fellowship of the Ring', 'director': 'Peter Jackson', 'genre': 'adventure'},
    {'title': 'Titanic', 'director': 'James Cameron', 'genre': 'romance'},
    {'title': 'Interstellar', 'director': 'Christopher Nolan', 'genre': 'sci-fi'},
    {'title': 'Django Unchained', 'director': 'Quentin Tarantino', 'genre': 'western'},
    {'title': 'The Dark Knight Rises', 'director': 'Christopher Nolan', 'genre': 'action'},
    {'title': 'Jurassic Park', 'director': 'Steven Spielberg', 'genre': 'adventure'},
    {'title': 'Avatar', 'director': 'James Cameron', 'genre': 'action'},
]

# GET Movies
@app.get("/movies/", response_model=List[Movie])
async def get_movies(director: Optional[str] = Query(None, alias='Director'), genre: Optional[str] = Query(None, alias='Genre')):
    if director and genre:
        filtered_movies = [movie for movie in MOVIES if director.lower() in movie['director'].lower() and genre.lower() in movie['genre'].lower()]
    elif director:
        filtered_movies = [movie for movie in MOVIES if director.lower() in movie['director'].lower()]
    elif genre:
        filtered_movies = [movie for movie in MOVIES if genre.lower() in movie['genre'].lower()]
    else:
        filtered_movies = MOVIES
    return filtered_movies

# POST Movie
@app.post("/movies/", response_model=Movie)
async def create_movie(movie: Movie):
    MOVIES.append(movie.dict())
    return movie

# PUT Movie
@app.put("/movies/{movie_name}", response_model=Movie)
async def update_movie(movie_name: str, updated_movie: Movie):
    for index, movie in enumerate(MOVIES):
        if movie['title'] == movie_name:
            MOVIES[index] = updated_movie.dict()
            return updated_movie
    raise HTTPException(status_code=404, detail="Movie not found")

# DELETE Movie
@app.delete("/movies/{movie_id}", response_model=Movie)
async def delete_movie(movie_id: int):
    if 0 <= movie_id < len(MOVIES):
        deleted_movie = MOVIES.pop(movie_id)
        return deleted_movie
    raise HTTPException(status_code=404, detail="Movie not found")