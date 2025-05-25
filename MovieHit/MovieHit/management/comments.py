from django.db import models # Importing models from Django's database models module
from django.contrib.auth.models import User # Importing User model from Django's authentication system
from django.core.validators import MinValueValidator, MaxValueValidator # Importing validators for rating field
from MovieHit.management.movies import Movies # Importing Movies model from the movies module in management package

class Comment(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='comments') # ForeignKey to Movies model, allowing multiple comments per movie
    user = models.ForeignKey(User, on_delete=models.CASCADE) # ForeignKey to User model, linking each comment to a user
    text = models.TextField() # Text field for the comment content
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]) # Rating field with a default value of 0, allowing values between 0 and 10
    created_at = models.DateTimeField(auto_now_add=True) # DateTime field to store when the comment was created, automatically set to the current date and time on creation
    
    class Meta: # Meta class to define additional properties of the model
        ordering = ['-created_at'] # Default ordering of the model instances by creation date, newest first
        
    def __str__(self): # String representation of the model instance, returning a summary of the comment
        return f'Comment by {self.user.username} on {self.movie.name}' # String representation of the Comment model
