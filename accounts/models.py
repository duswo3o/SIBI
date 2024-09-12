from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female")]

    email = models.EmailField(blank=True, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birthday = models.DateField()

    def __str__(self):
        return self.username
