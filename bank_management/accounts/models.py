from django.db import models
from django.contrib.auth.models import User
import random
from .constants import ACCOUNT_TYPE, GENDER_TYPE
# Create your models here.


class BankAccountPersonal(models.Model):
    user = models.OneToOneField(
        User, related_name='account', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    account_no = account_no = models.CharField(
        max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.account_no:
            self.account_no = self.generate_account_no()
        super(BankAccountPersonal, self).save(*args, **kwargs)

    def generate_account_no(self):
        while True:
            account_no = str(random.randint(1000000000, 9999999999))
            if not BankAccountPersonal.objects.filter(account_no=account_no).exists():
                return account_no

    birth_date = models.DateTimeField()
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    initial_deposit_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.account_no}"


class BankAccountAddress(models.Model):
    user = models.OneToOneField(
        User, related_name="address", on_delete=models.CASCADE)

    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    county = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.user.email}"
