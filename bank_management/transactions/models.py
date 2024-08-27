from django.db import models
from accounts.models import BankAccountPersonal
from .constants import TRANSACTION_TYPE
# Create your models here.

class Transactions(models.Model):
    account = models.ForeignKey(BankAccountPersonal, related_name='transactions', on_delete= models.CASCADE, null=True)

    amount = models.DecimalField( max_digits=10, decimal_places=2)
    balance_after_transaction = models.DecimalField( max_digits=10, decimal_places=2)
    Transaction_type = models.IntegerField(choices=TRANSACTION_TYPE,null=True)
    time_tamp = models.DateTimeField( auto_now_add=True)
    loan_approved = models.BooleanField( default=False)

    class Meta:
        ordering =['time_tamp']

