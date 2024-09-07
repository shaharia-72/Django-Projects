from django.db import models

# Create your models here.

class BooksCategory(models.Model):
    books_category = models.CharField(max_length=50)

    def __str__(self):
        return self.books_category
