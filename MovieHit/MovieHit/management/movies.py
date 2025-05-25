from django.db import models # Importing models from Django's database models module
from simple_history.models import HistoricalRecords # Importing HistoricalRecords for tracking changes in the model
import base64 # Importing base64 for encoding unique IDs
import uuid # Importing uuid for generating unique identifiers
   
class Movies(models.Model):
    name = models.CharField(max_length=200, default="No name", help_text="The name of the movie.") # Field for the name of the movie
    year = models.IntegerField(default="No year", help_text="The release year of the movie.") # Field for the release year of the movie
    length = models.IntegerField(default="No length", help_text="The length of the movie in minutes.") # Field for the length of the movie in minutes
    rating = models.FloatField(default="No rating", help_text="The rating of the movie (e.g., IMDb rating).") # Field for the movie rating
    genres = models.JSONField(default=dict, help_text="A list of genres associated with the movie.") # Field for storing genres as a JSON object
    age = models.CharField(max_length=50, default="No age", help_text="The age rating of the movie (e.g., PG-13).") # Field for the age rating of the movie
    directors = models.JSONField(default=dict, help_text="A list of directors of the movie.") # Field for storing directors as a JSON object
    writers = models.JSONField(default=dict, help_text="A list of writers of the movie.") # Field for storing writers as a JSON object
    actors = models.JSONField(default=dict, help_text="A list of actors in the movie.") # Field for storing actors as a JSON object
    description = models.CharField(max_length=400, default="No description", help_text="The description of the movie.") # Field for the movie description
    trailer = models.URLField(max_length=200, default="No trailer", help_text="The URL of the movie's trailer.") # Field for the movie trailer URL
    unique_id = models.CharField(max_length=50, blank=True, null=True, unique=True, help_text="Unique ID for the movie URL") # Field for storing a unique identifier for the movie, used in URLs
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, help_text="Upload a poster image for the movie.") # Image field for the movie poster, allowing blank and null values
    history = HistoricalRecords() # HistoricalRecords to keep track of changes made to the model instances

    def __str__(self): # String representation of the model instance, returning the name of the movie
        return self.name # String representation of the Movies model

    def save(self, *args, **kwargs): # Override the save method to generate a unique ID if it doesn't exist
        if not self.unique_id: # Check if unique_id is not set
            base_string = f"{self.id if self.id else uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:6]}" # Create a base string using the movie ID or a new UUID
            encoded = base64.urlsafe_b64encode(base_string.encode()).decode().rstrip('=') # Encode the base string to a URL-safe base64 string and remove padding
            self.unique_id = encoded[:10] # Truncate to 10 characters to ensure it fits within the field length
        super().save(*args, **kwargs) # Call the parent save method to save the instance


    class Meta: # Meta class to define additional properties of the model
        verbose_name_plural = "Movies" # Plural name for the model in the admin interface
        ordering = ['-year', 'name'] # Default ordering of the model instances by year (newest first) and then by name
