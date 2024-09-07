from django import forms
from .models import BooksCategory


class BooksCategory(forms.ModelForm):
    
    class Meta:
        model = BooksCategory
        fields = ['name']
