from django.db import models
from simple_history.models import HistoricalRecords
import base64
import uuid
   
class Movies(models.Model):
    name = models.CharField(max_length=200, default="No name", help_text="The name of the movie.")
    year = models.IntegerField(default="No year", help_text="The release year of the movie.")
    length = models.IntegerField(default="No length", help_text="The length of the movie in minutes.")
    rating = models.FloatField(default="No rating", help_text="The rating of the movie (e.g., IMDb rating).")
    genres = models.JSONField(default=dict, help_text="A list of genres associated with the movie.")
    age = models.CharField(max_length=50, default="No age", help_text="The age rating of the movie (e.g., PG-13).")
    directors = models.JSONField(default=dict, help_text="A list of directors of the movie.")
    writers = models.JSONField(default=dict, help_text="A list of writers of the movie.")
    actors = models.JSONField(default=dict, help_text="A list of actors in the movie.")
    description = models.CharField(max_length=400, default="No description", help_text="The description of the movie.")
    trailer = models.URLField(max_length=200, default="No trailer", help_text="The URL of the movie's trailer.")
    unique_id = models.CharField(max_length=50, blank=True, null=True, unique=True, help_text="Unique ID for the movie URL")
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, help_text="Upload a poster image for the movie.")
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate a unique ID if one doesn't exist
        if not self.unique_id:
            # Create a base string from movie ID and a UUID
            base_string = f"{self.id if self.id else uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:6]}"
            # Encode to base64 and remove padding
            encoded = base64.urlsafe_b64encode(base_string.encode()).decode().rstrip('=')
            self.unique_id = encoded[:10]  # Limit to 10 characters
        super().save(*args, **kwargs)


    class Meta:
        verbose_name_plural = "Movies"
        ordering = ['-year', 'name']
