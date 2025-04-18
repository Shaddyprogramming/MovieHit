import json
import os
from django.shortcuts import render
from django.http import JsonResponse
from MovieHit.management.movie_models import Movies


# Path to the movies.json file
MOVIES_JSON_PATH = os.path.join(os.path.dirname(__file__), '../data/movies.json')

def load_movies():
    """Load movies from the JSON file."""
    if os.path.exists(MOVIES_JSON_PATH):
        with open(MOVIES_JSON_PATH, 'r') as file:
            return json.load(file)
    return []

def save_movies(movies_data):
    """Save movies to the JSON file."""
    with open(MOVIES_JSON_PATH, 'w') as file:
        json.dump(movies_data, file, indent=4)

def index(request):
    """Render the homepage with a list of movies."""
    query = request.GET.get('q', '')  # Get the search query from the request
    movies_data = load_movies()

    if query:
        # Filter movies by name (case-insensitive)
        filtered_movies = [
            movie for movie in movies_data if query.lower() in movie['name'].lower()
        ]
    else:
        filtered_movies = movies_data

    return render(request, 'index.html', {'movies': filtered_movies, 'query': query})

def add_movie(request):
    """Add a new movie to the JSON file."""
    if request.method == 'POST':
        # Extract movie data from the POST request
        name = request.POST.get('name')
        director = request.POST.get('director')
        rating = float(request.POST.get('rating', 0))
        genres = request.POST.getlist('genres')  # Expecting genres as a list
        length_in_minutes = int(request.POST.get('length_in_minutes', 0))

        # Create a new movie instance
        try:
            new_movie = Movies(name, director, rating, genres, length_in_minutes)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Load existing movies and add the new one
        movies_data = load_movies()
        movies_data.append(new_movie.to_dict())
        save_movies(movies_data)

        return JsonResponse({'message': 'Movie added successfully!'})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def delete_movie(request, movie_name):
    """Delete a movie from the JSON file."""
    if request.method == 'POST':
        movies_data = load_movies()
        updated_movies = [movie for movie in movies_data if movie['name'] != movie_name]

        if len(updated_movies) == len(movies_data):
            return JsonResponse({'error': 'Movie not found.'}, status=404)

        save_movies(updated_movies)
        return JsonResponse({'message': 'Movie deleted successfully!'})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
