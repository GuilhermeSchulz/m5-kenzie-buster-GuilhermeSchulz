from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import MovieOrder, Movie


class User(AbstractUser):
    email = models.CharField(max_length=127, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_employee = models.BooleanField(default=False, null=True)
    birthdate = models.DateField(null=True)
