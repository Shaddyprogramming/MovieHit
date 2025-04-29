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
    history = HistoricalRecords()
    #TODO 1
    # un model pentru numarul de comentarii
    #TODO 2
    # un model pentru numarul de review-uri
    #TODO 3
    # un model pentru descriere

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Movies"
        ordering = ['-year', 'name']
