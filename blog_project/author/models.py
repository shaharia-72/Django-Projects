from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=30)
    bio = models.TextField()
    author_phone = models.CharField(max_length=12)

    def __str__(self) -> str:
        return self.name
