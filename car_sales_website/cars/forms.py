from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']


class OrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Quantity')
