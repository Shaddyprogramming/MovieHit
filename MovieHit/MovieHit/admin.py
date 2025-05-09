from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from simple_history.admin import SimpleHistoryAdmin
from .management.movies import Movies
from .management.banners import Banners
import pytz

@admin.register(Movies)
class MoviesAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'year', 'length', 'rating', 'show_genres', 'formatted_history') 
    search_fields = ('name', 'year', 'rating')
   
    list_filter = ('year', 'rating', 'length')
    
    ordering = ( 'name','-year', 'length', 'rating', 'genres', 'actors', 'writers', 'directors')

    def show_genres(self, obj):
        if not obj.genres:
            return "No genres"
        return ", ".join(obj.genres) if isinstance(obj.genres, list) else str(obj.genres)

    show_genres.short_description = 'Genres'

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

        return None

    formatted_history.short_description = 'History'
    
@admin.register(Banners)
class BannersAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'formatted_history') 
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)

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

        return None

    formatted_history.short_description = 'History'
