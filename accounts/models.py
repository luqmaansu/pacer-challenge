from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    remarks = models.TextField(blank=True)