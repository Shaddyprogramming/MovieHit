import json
import os

class Movies:
    def __init__(self, name: str, year: int, length: int, rating: float, genres: list[str], age: str, directors: list[str], writers: list[str], actors: list[str]) :
        if len(genres) > 5:
            raise ValueError("A movie can have a maximum of 5 genres.")
        if len(directors) > 5:
            raise ValueError("A movie can have a maximum of 5 directors.")
        if len(writers) > 5:
            raise ValueError("A movie can have a maximum of 5 writers.")
        if len(actors) > 5:
            raise ValueError("A movie can have a maximum of 5 actors.")
        
        self.name = name
        self.year=year
        self.length = length
        self.rating = rating
        self.genres = genres
        self.age=age
        self.directors = directors
        self.writers=writers
        self.actors=actors   

    def to_dict(self):
        """Convert the movie object to a dictionary."""
        return {
            "name": self.name,
            "year": self.year,
            "length": self.length,
            "rating": self.rating,
            "genres": self.genres,
            "age": self.age,
            "directors": self.directors,
            "writers": self.writers,
            "actors": self.actors,
        }

    @staticmethod
    def add_movie_to_json(movie, file_path="../data/movies.json"):
        """Add a movie to the JSON file."""
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        
        # Load existing data
        if os.path.exists(full_path):
            with open(full_path, "r") as file:
                movies_data = json.load(file)
        else:
            movies_data = []

        # Append the new movie
        movies_data.append(movie.to_dict())

        # Write back to the file
        with open(full_path, "w") as file:
            json.dump(movies_data, file, indent=4)