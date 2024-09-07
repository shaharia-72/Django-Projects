from django.contrib import admin
from .models import BankAccountPersonal, BankAccountAddress
# Register your models here.



admin.site.register(BankAccountAddress)
@admin.register(BankAccountPersonal)
class BankAccountPersonalAdmin(admin.ModelAdmin):
    list_display = ['user_full_name', 'account_type', 'account_no']

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"  # Concatenate first name and last name
    
    user_full_name.short_description = 'Full Name' 