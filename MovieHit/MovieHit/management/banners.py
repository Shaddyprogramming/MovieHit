from django.db import models
from simple_history.models import HistoricalRecords
   
class Banners(models.Model):
    name = models.CharField(max_length=200, help_text="The name of the movie.")
    active = models.BooleanField(default=False, help_text="Is the banner active?")
    banner_img = models.ImageField(upload_to='banners/', blank=True, null=True, help_text="Upload a banner image for the movie.")
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Banners"
        ordering = ['name']
