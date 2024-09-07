from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PersonalAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.DecimalField(default=499.00, max_digits=8, decimal_places=2)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Profile"