from django.db import models
from brands.models import Brand
from django.contrib.auth.models import User

# Create your models here.


class Car(models.Model):
    car_image = models.ImageField(upload_to='cars/media/car_images/')
    car_title = models.CharField(max_length=200)
    car_descriptions = models.TextField()
    car_price = models.DecimalField(max_digits=10, decimal_places=2)
    car_quantity = models.PositiveBigIntegerField(default=1)
    car_add_time = models.DateTimeField(auto_now_add=True)
    brand = models.ForeignKey(
        Brand, related_name="cars", on_delete=models.CASCADE)

    def __str__(self):
        return self.car_title


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment_add_time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    car = models.ForeignKey(Car, related_name='comments',
                            on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}: {self.comment}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    OrderTime = models.DateTimeField(auto_now_add=True)
