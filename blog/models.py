from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(AbstractUser):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    bio = models.TextField(max_length=1200, verbose_name='Bio', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    owner = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255)
    full_description = models.TextField()
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
