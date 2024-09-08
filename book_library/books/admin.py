from django.contrib import admin
from .models import Books, BorrowBooks, RentalBooks, Coupon


# Register your models here.
admin.site.register(Books)
admin.site.register(BorrowBooks)
admin.site.register(RentalBooks)
admin.site.register(Coupon)
