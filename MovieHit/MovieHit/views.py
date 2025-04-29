from django.shortcuts import render
from MovieHit.management.movies import Movies

def index(request):
    query = request.GET.get('q', '')

    if query:
        movies_data = Movies.objects.filter(name__icontains=query)
    else:
        movies_data = Movies.objects.all()

    return render(request, 'index.html', {'movies': movies_data, 'query': query})

