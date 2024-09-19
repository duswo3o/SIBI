from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female")]

    email = models.EmailField(blank=True, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birthday = models.DateField()

    followings = models.ManyToManyField(
        to="self", related_name="followers", symmetrical=False, blank=True
    )

    def __str__(self):
        return self.username
