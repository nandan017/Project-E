from django.db import models

from django.db import models
from election.models import Candidate

class Vote(models.Model):
    timestamp = models.DateTimeField(auto_now_add=False)
    student_id = models.CharField(max_length=50, unique=True)
    
    # Use the unique key as the ForeignKey reference
    candidate = models.ForeignKey(Candidate, to_field='candidate_key', on_delete=models.CASCADE)
    
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)

    def __str__(self):
        return f'Vote by {self.student_id} for {self.candidate.name}'
