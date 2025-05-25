from django.db import models # Importing models from Django's database models module
from simple_history.models import HistoricalRecords # Importing HistoricalRecords for tracking changes in the model
   
class Banners(models.Model): # Defining the Banners model to represent movie banners
    name = models.CharField(max_length=200, help_text="The name of the movie.") # Field for the name of the movie banner
    active = models.BooleanField(default=False, help_text="Is the banner active?") # Boolean field to indicate if the banner is active
    banner_img = models.ImageField(upload_to='banners/', blank=True, null=True, help_text="Upload a banner image for the movie.") # Image field for the banner image, allowing blank and null values
    history = HistoricalRecords() # HistoricalRecords to keep track of changes made to the model instances

    def __str__(self): # String representation of the model instance, returning the name of the banner
        return self.name # String representation of the Banners model

    class Meta: # Meta class to define additional properties of the model
        verbose_name_plural = "Banners" # Plural name for the model in the admin interface
        ordering = ['name'] # Default ordering of the model instances by name
