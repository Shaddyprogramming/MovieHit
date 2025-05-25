from django.contrib import admin # Importing the admin module from Django's contrib package
from django.contrib.auth.admin import UserAdmin # Importing UserAdmin to customize the User model in the admin interface
from django.contrib.auth.models import User # Importing User model from Django's authentication system
from simple_history.admin import SimpleHistoryAdmin # Importing SimpleHistoryAdmin to manage historical records in the admin interface
from .management.movies import Movies # Importing Movies model from the movies module in management package
from .management.banners import Banners # Importing Banners model from the banners module in management package
from .management.comments import Comment # Importing Comment model from the comments module in management package
import pytz # Importing pytz for timezone handling

@admin.register(Movies) # Registering the Movies model with the admin interface
class MoviesAdmin(SimpleHistoryAdmin): # Customizing the admin interface for the Movies model
    list_display = ('name', 'year', 'length', 'rating', 'show_genres', 'formatted_history')  # Displayed fields in the admin list view
    search_fields = ('name', 'year', 'rating') # Fields to search in the admin interface
   
    list_filter = ('year', 'rating', 'length') # Fields to filter the list view in the admin interface
    
    ordering = ('name', '-year', 'length', 'rating') # Default ordering of the list view in the admin interface

    def show_genres(self, obj): # Method to display genres in a formatted way
        if not obj.genres: # Check if genres is empty or None
            return "No genres" # Return a default message if no genres are available
        return ", ".join(obj.genres) if isinstance(obj.genres, list) else str(obj.genres) # Join genres with a comma if it's a list, otherwise convert to string

    show_genres.short_description = 'Genres' # Short description for the genres field in the admin interface

    def formatted_history(self, obj): 
        """
        Display the most recent history entry in the desired format.
        If no history is available, return None.
        """
        if hasattr(obj, 'history') and obj.history.exists(): # Check if the object has history and if it exists
            latest_history = obj.history.first() # Get the most recent history entry
            history_date = latest_history.history_date.astimezone(pytz.timezone('Europe/Bucharest')) # Convert history date to Bucharest timezone
            formatted_date = history_date.strftime('%B %d, %Y, %I:%M %p') # Format the date in a readable way
            changed_by = latest_history.history_user.username if latest_history.history_user else "Unknown" # Get the username of the user who made the change, or "Unknown" if not available
            comment = "Created" if latest_history.history_type == "+" else "Modified" # Determine the type of change (created or modified)
            return f"{formatted_date} | {comment} | {changed_by}" # Return the formatted history entry

        return None # Return None if no history is available

    formatted_history.short_description = 'History' # Short description for the history field in the admin interface
    
@admin.register(Banners) # Registering the Banners model with the admin interface
class BannersAdmin(SimpleHistoryAdmin): # Customizing the admin interface for the Banners model
    list_display = ('name', 'formatted_history')  # Displayed fields in the admin list view
    search_fields = ('name',) # Fields to search in the admin interface
    list_filter = ('name',) # Fields to filter the list view in the admin interface
    ordering = ('name',) # Default ordering of the list view in the admin interface

    def formatted_history(self, obj):
        """
        Display the most recent history entry in the desired format.
        If no history is available, return None.
        """
        if hasattr(obj, 'history') and obj.history.exists(): # Check if the object has history and if it exists
            latest_history = obj.history.first() # Get the most recent history entry 
            history_date = latest_history.history_date.astimezone(pytz.timezone('Europe/Bucharest')) # Convert history date to Bucharest timezone
            formatted_date = history_date.strftime('%B %d, %Y, %I:%M %p') # Format the date in a readable way
            changed_by = latest_history.history_user.username if latest_history.history_user else "Unknown" # Get the username of the user who made the change, or "Unknown" if not available
            comment = "Created" if latest_history.history_type == "+" else "Modified" # Determine the type of change (created or modified)
            return f"{formatted_date} | {comment} | {changed_by}" # Return the formatted history entry

        return None # Return None if no history is available

    formatted_history.short_description = 'History' # Short description for the history field in the admin interface

@admin.register(Comment) # Registering the Comment model with the admin interface
class CommentAdmin(admin.ModelAdmin): # Customizing the admin interface for the Comment model
    list_display = ('user', 'movie', 'rating', 'short_text', 'created_at') # Displayed fields in the admin list view
    list_filter = ('rating', 'created_at', 'movie') # Fields to filter the list view in the admin interface
    search_fields = ('text', 'user__username', 'movie__name') # Fields to search in the admin interface
    ordering = ('-created_at',) # Default ordering of the list view in the admin interface
    
    def short_text(self, obj): # Method to display a shortened version of the comment text
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text # Return the first 50 characters of the comment text, followed by '...' if it's longer than 50 characters
    
    short_text.short_description = 'Comment' # Short description for the comment field in the admin interface
