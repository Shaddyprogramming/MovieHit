import json
from django.shortcuts import render
import os

def index(request):
    # Load movies from the JSON file
    file_path = os.path.join(os.path.dirname(__file__), "../data/movies.json")
    with open(file_path, "r") as file:
        movies = json.load(file)
    
    # Pass movies to the template
    return render(request, "index.html", {"movies": movies})
