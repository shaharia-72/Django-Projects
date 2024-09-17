from django import forms
from .models import Event, Participant

class InterestForm(forms.Form):
    number_of_participants = forms.IntegerField(min_value=1, label="Number of participants")

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_title', 'event_description', 'event_location', 'event_image', 'event_ticket_price', 'event_registration_start', 'event_registration_end', 'event_start_date', 'event_max_participants', 'category']
