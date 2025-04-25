from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin  # Import SimpleHistoryAdmin
from .management.movies import Movies  # Import the Django model
from datetime import datetime
import pytz  # Import pytz for time zone handling

@admin.register(Movies)
class MoviesAdmin(SimpleHistoryAdmin):  # Use SimpleHistoryAdmin for history tracking
    list_display = ('name', 'year', 'length', 'rating', 'show_genres', 'formatted_history')  # Add formatted_history
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

    def formatted_history(self, obj):
        """
        Display the most recent history entry in the desired format.
        If no history is available, return None.
        """
        if hasattr(obj, 'history') and obj.history.exists():
            latest_history = obj.history.first()
            history_date = latest_history.history_date.astimezone(pytz.timezone('Europe/Bucharest'))
            formatted_date = history_date.strftime('%B %d, %Y, %I:%M %p')
            changed_by = latest_history.history_user.username if latest_history.history_user else "Unknown"
            comment = "Created" if latest_history.history_type == "+" else "Modified"
            return f"{formatted_date} | {comment} | {changed_by}"

        return None  # No default value if no history exists

    formatted_history.short_description = 'History'  # Set the column header for the admin panel
