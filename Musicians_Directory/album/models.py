from django.db import models
from django.utils.translation import gettext_lazy as _
from musician.models import Musician

# Create your models here.


class Album(models.Model):
    album_name = models.CharField(max_length=20)
    album_release_date = models.DateField(
        _("Date Time"), auto_now=False, auto_now_add=False)
    rating = models.IntegerField(
        _("Rating"), choices=[(i, i) for i in range(1, 6)], default=1)
    music = models.ForeignKey(Musician, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.album_name} - {self.album_release_date}"
