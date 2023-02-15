from django.db import models

# Create your models here.


class Ratings(models.TextChoices):
    GRATING = "G"
    PG = "PG"
    PG13 = "PG-13"
    RRATING = "R"
    NC17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True)
    rating = models.CharField(
        max_length=20, choices=Ratings.choices, default=Ratings.GRATING
    )
    synopsis = models.TextField(null=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="movies"
    )
