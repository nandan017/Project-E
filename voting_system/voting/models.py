from django.db import models
from election.models import Candidate

class Vote(models.Model):
    timestamp = models.DateTimeField(auto_now_add=False)
    student_id = models.CharField(max_length=50, unique=True)
    
    # Use the unique key as the ForeignKey reference
    candidates = models.ManyToManyField(Candidate)    
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)

    def __str__(self):
        return f'Vote by {self.student_id}'
