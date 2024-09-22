from django.db import models

from django.db import models
import uuid  # Import UUID module for generating unique keys

class Candidate(models.Model):
    # Unique identifier
    candidate_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    name = models.CharField(max_length=100)
    forum = models.CharField(max_length=100)
    image = models.ImageField(upload_to='candidate_images/', blank=True, null=True)  # New field for the candidate's image


    def __str__(self):
        return f'{self.name} ({self.forum})'
