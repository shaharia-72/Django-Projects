from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Musician(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=12)
    instrument_name = models.CharField(max_length=100)
    # phone_number = PhoneNumberField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
