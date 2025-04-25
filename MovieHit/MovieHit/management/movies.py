from django.db import models
from simple_history.models import HistoricalRecords
  
class Movies(models.Model):
    """
    Represents a movie with various attributes such as name, year, length, rating, genres, and more.
    """
    name = models.CharField(max_length=200, help_text="The name of the movie.")
    year = models.IntegerField(help_text="The release year of the movie.")
    length = models.IntegerField(help_text="The length of the movie in minutes.")  # Assuming length is in minutes
    rating = models.FloatField(help_text="The rating of the movie (e.g., IMDb rating).")
    genres = models.JSONField(help_text="A list of genres associated with the movie.")  # Stores a list of genres
    age = models.CharField(max_length=50, help_text="The age rating of the movie (e.g., PG-13).")
    directors = models.JSONField(help_text="A list of directors of the movie.")  # Stores a list of directors
    writers = models.JSONField(help_text="A list of writers of the movie.")  # Stores a list of writers
    actors = models.JSONField(help_text="A list of actors in the movie.")  # Stores a list of actors
    history = HistoricalRecords()  # Add this line to enable history tracking

    def __str__(self):
        """
        Returns the string representation of the movie, which is its name.
        """
        return self.name

    class Meta:
        verbose_name_plural = "Movies"  # Explicitly set the plural name for the admin panel
        ordering = ['-year', 'name']  # Default ordering by year (descending) and name (ascending)
