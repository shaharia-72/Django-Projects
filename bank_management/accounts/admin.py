from django.contrib import admin
from .models import BankAccountPersonal, BankAccountAddress
# Register your models here.


admin.site.register(BankAccountPersonal)
admin.site.register(BankAccountAddress)
