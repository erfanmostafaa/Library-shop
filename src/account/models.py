from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    genre = models.CharField(max_length= 100)

    class Meta:
        unique_together = ('title', 'author', 'genre')

    def __str__(self):
        return f"{self.title} by {self.author}"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('book', 'user')
        constraints = [
            models.CheckConstraint(check = models.Q(rating__gte = 1, rating__lte = 5), name = 'rating_range')
        ]



class User(AbstractUser):
    pass