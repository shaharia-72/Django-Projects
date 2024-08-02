from django import forms


class contact_form(forms.Form):
    name = forms.CharField(label='User name')
    file = forms.FileField(label='File upload')
    # email = forms.EmailField(label='User email')
    # age = forms.IntegerField(label='User age')
    # age = forms.IntegerField()
    # weight = forms. FloatField()
    # balance = forms.DecimalField()
    # check = forms.BooleanField()
    # birthday = forms.DateField()
    # appointment = forms.DateTimeField()
    # CHOICES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]
    # size = forms.ChoiceField(choices=CHOICES)
    # MEAL = [('P', 'Pepperoni'), ('M', 'Mashroom'), ('B', 'Beef')]
    # pizza = forms. MultipleChoiceField(choices=MEAL)
