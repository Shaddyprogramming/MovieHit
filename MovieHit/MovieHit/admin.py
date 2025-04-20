from django.contrib import admin
from .management.movies import Movies  # Import the Django model

@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'length', 'rating', 'show_genres')  # Fields to display in the admin list view
    search_fields = ('name', 'year', 'rating')  # Enable search functionality
    list_filter = ('year', 'rating')  # Add filters for year and rating
    ordering = ('-year', 'name')  # Default ordering by year (descending) and name

    def show_genres(self, obj):
        """
        Display genres as a comma-separated string in the admin panel.
        Handles cases where genres might be None or not a list.
        """
        if not obj.genres:
            return "No genres"
        return ", ".join(obj.genres) if isinstance(obj.genres, list) else str(obj.genres)
    
    show_genres.short_description = 'Genres'  # Set the column header for the admin panel
