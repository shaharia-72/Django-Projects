from django.db import models

# Create your models here.
from categories.models import Category
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    # many to many relationships => one post can have many categories and many categories can have one posts
    category = models.ManyToManyField(Category)
    # one to many relationship =>one author can have many posts and many post can have one author
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.title
