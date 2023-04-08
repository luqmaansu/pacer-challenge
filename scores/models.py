from django.db import models
from accounts.models import User
from django.utils import timezone

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    score = models.FloatField(default=0)
    date_submitted = models.DateTimeField(default=timezone.now)