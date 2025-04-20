from django.shortcuts import render
from MovieHit.management.movies import Movies

def index(request):
    """Render the homepage with a list of movies from the database."""
    query = request.GET.get('q', '')  # Get the search query from the request

    # Query the database for movies
    if query:
        # Filter movies by name (case-insensitive)
        movies_data = Movies.objects.filter(name__icontains=query)
    else:
        # Retrieve all movies
        movies_data = Movies.objects.all()

    return render(request, 'index.html', {'movies': movies_data, 'query': query})

