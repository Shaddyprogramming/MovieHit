import json
import os

class Movies:
    def __init__(self, name: str, director: str, rating: float, genres: list[str], length_in_minutes: int):
        if len(genres) > 5:
            raise ValueError("A movie can have a maximum of 5 genres.")
        
        self.name = name
        self.director = director
        self.rating = rating
        self.genres = genres
        self.length_in_minutes = length_in_minutes

    def __str__(self):
        return (f"Movie: {self.name}, Directed by: {self.director}, "
                f"Rating: {self.rating}, Genres: {', '.join(self.genres)}, "
                f"Length: {self.length_in_minutes} minutes")

    def to_dict(self):
        """Convert the movie object to a dictionary."""
        return {
            "name": self.name,
            "director": self.director,
            "rating": self.rating,
            "genres": self.genres,
            "length_in_minutes": self.length_in_minutes
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

# Example usage
if __name__ == "__main__":
    new_movie = Movies(
        name="Avatar",
        director="James Cameron",
        rating=7.8,
        genres=["Sci-Fi", "Adventure", "Fantasy"],
        length_in_minutes=162
    )
    Movies.add_movie_to_json(new_movie)
    print(f"Added movie: {new_movie}")
