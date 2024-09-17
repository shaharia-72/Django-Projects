from django.db import models
from accounts.models import Organizer, Participant
import random
import string


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, blank=True, editable=False)

    def generate_slug(self, name):
        slug = name.replace(" ", "-")
        unique_slug = slug
        counter = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug   
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug(self.category_name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.category_name

class Event(models.Model):
    category = models.ManyToManyField(Category)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=11, unique=True, default=''.join(random.choices(string.ascii_uppercase, k=4)) + '-' + ''.join(random.choices(string.digits, k=6)))
    event_title = models.CharField(max_length=50)
    event_description = models.TextField()
    event_location = models.CharField(max_length=50)
    event_max_participants = models.PositiveIntegerField()
    event_image = models.ImageField(upload_to='events_images/',blank=True, null=True)
    event_ticket_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    event_registration_start = models.DateTimeField()
    event_registration_end = models.DateTimeField()
    event_start_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if  self.event_id:
            self.event_id = self.generate_unique_event_id()
        super().save(*args, **kwargs)

    def generate_unique_event_id(self):
        while True:
            random_id = ''.join(random.choices(string.ascii_uppercase, k=4)) + '-' + ''.join(random.choices(string.digits, k=6))
            if not Event.objects.filter(event_id=random_id).exists():
                return random_id

    def __str__(self):
        return self.event_title


class Participation(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    transition_id = models.CharField(max_length=11, default=''.join(random.choices(string.ascii_uppercase, k=4)) + '-' + ''.join(random.choices(string.digits, k=6)))
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('confirmed', 'Confirmed')))
    number_of_participants = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.participant.user.username} - {self.event.event_title}"
