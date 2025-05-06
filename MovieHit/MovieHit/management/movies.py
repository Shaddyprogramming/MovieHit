from django.db import models
from simple_history.models import HistoricalRecords
   
class Movies(models.Model):
    name = models.CharField(max_length=200, help_text="The name of the movie.")
    year = models.IntegerField(help_text="The release year of the movie.")
    length = models.IntegerField(help_text="The length of the movie in minutes.")
    rating = models.FloatField(help_text="The rating of the movie (e.g., IMDb rating).")
    genres = models.JSONField(help_text="A list of genres associated with the movie.")
    age = models.CharField(max_length=50, help_text="The age rating of the movie (e.g., PG-13).")
    directors = models.JSONField(help_text="A list of directors of the movie.")
    writers = models.JSONField(help_text="A list of writers of the movie.")
    actors = models.JSONField(help_text="A list of actors in the movie.")
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, help_text="Upload a poster image for the movie.")
    history = HistoricalRecords()

    #TODO 1
    # un model pentru descriere

    #TODO NU STIU
    # un model pentru linkuri youtube trailer

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Movies"
        ordering = ['-year', 'name']
