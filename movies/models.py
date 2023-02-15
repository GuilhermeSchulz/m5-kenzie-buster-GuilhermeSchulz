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
    movie_orders = models.ManyToManyField(
        "users.User", through="MovieOrder", related_name="movie"
    )


class MovieOrder(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} comprou {self.movie.title} por {self.price}"
