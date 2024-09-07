from django.db import models
from django.contrib.auth.models import User
from books_categories.models import BooksCategory 
from datetime import timedelta
from django.utils import timezone
# Create your models here.


class Books(models.Model):
    books_image = models.ImageField(upload_to='books_images/')
    books_author_name = models.CharField(max_length=20,null=True)
    books_title = models.CharField(max_length=200)
    books_ISBN = models.CharField(max_length=25, unique=True, null=True)
    books_descriptions = models.TextField()
    books_price = models.DecimalField(max_digits=10, decimal_places=2)
    books_quantity = models.PositiveBigIntegerField(default=1)
    books_add_time = models.DateTimeField(auto_now_add=True)
    books_category = models.ForeignKey(
        BooksCategory, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return self.books_title

class BorrowBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    email = models.EmailField()
    quantity = models.PositiveIntegerField(default=1)
    rental_days = models.PositiveIntegerField()
    borrowed_on = models.DateTimeField(auto_now_add=True)
    return_due_date = models.DateTimeField()
    returned_on = models.DateTimeField(null=True, blank=True)

    def is_returned_on_time(self):
        if self.returned_on:
            return self.returned_on <= self.return_due_date
        return False

    def overdue_days(self):
        if self.returned_on and self.returned_on > self.return_due_date:
            return (self.returned_on - self.return_due_date).days
        return 0

    def __str__(self):
        return f'{self.book.books_title} borrowed by {self.user.username}'

class RentalBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True,blank=True)
    rental_days = models.PositiveBigIntegerField(default=7)

    @property
    def due_date(self):
        return self.borrow_date + timedelta(days=self.rental_days)
    
    @property
    def is_late(self):
        if self.return_date:
            return self.return_date > self.due_date
        return False

    def __str__(self):
        return f"{self.user} - {self.book.title}"
