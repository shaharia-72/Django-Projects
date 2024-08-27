from typing import Any
from django.contrib.auth.forms import UserCreationForm
from .constants import ACCOUNT_TYPE, GENDER_TYPE
from django import forms
from django.contrib.auth.models import User
from .models import BankAccountPersonal, BankAccountAddress


# class UserRegistrationForm(forms.ModelForm):
class UserRegistrationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    birth_date = forms.DateTimeField(widget=forms.DateInput(attrs={"type": "date"}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=20)
    country = forms.CharField(max_length=20)
    postal_code = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "account_type",
            "birth_date",
            "gender",
            "street_address",
            "city",
            "country",
            "postal_code",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit == True:
            user.save()
            account_type = self.cleaned_data.get("account_type")
            # account_no = self.cleaned_data.get('account_no')
            birth_date = self.cleaned_data.get("birth_date")
            gender = self.cleaned_data.get("gender")
            # initial_deposit_date = self.cleaned_data.get(
            #     'initial_deposit_date'
            #     )

            street_address = self.cleaned_data.get("street_address")
            city = self.cleaned_data.get("city")
            postal_code = self.cleaned_data.get("postal_code")
            country = self.cleaned_data.get("country")

            BankAccountPersonal.objects.create(
                user=user,
                account_type=account_type,
                # account_no=account_no,
                birth_date=birth_date,
                gender=gender,
                # initial_deposit_date=initial_deposit_date,
            )

            BankAccountAddress.objects.create(
                user=user,
                street_address=street_address,
                city=city,
                postal_code=postal_code,
                country=country,
            )
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-gray-200 "
                        "text-gray-700 border border-gray-200 rounded "
                        "py-3 px-4 leading-tight focus:outline-none "
                        "focus:bg-white focus:border-gray-500"
                    )
                }
            )


class UserUpdateForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    birth_date = forms.DateTimeField(widget=forms.DateInput(attrs={"type": "date"}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=20)
    country = forms.CharField(max_length=20)
    postal_code = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ["username","first_name",
            "last_name",
            "email",
            "account_type",
            "birth_date",
            "gender",
            "street_address",
            "city",
            "country",
            "postal_code",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-gray-200 "
                        "text-gray-700 border border-gray-200 rounded "
                        "py-3 px-4 leading-tight focus:outline-none "
                        "focus:bg-white focus:border-gray-500"
                    )
                }
            )
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({'readonly': 'readonly'})

        # if 'account_type' in self.fields:
        #     self.fields['account_type'].widget.attrs.update({'disabled': 'disabled'})

        # if 'gender' in self.fields:
        #     self.fields['gender'].widget.attrs.update({'disabled': 'disabled'})


        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except:
                user_account = None
                user_address = None

            if user_account:
                self.fields["account_type"].initial = user_account.account_type
                self.fields["birth_date"].initial = user_account.birth_date
                self.fields["gender"].initial = user_account.gender

            if user_address:    
                self.fields["street_address"].initial = user_address.street_address
                self.fields["city"].initial = user_address.city
                self.fields["country"].initial = user_address.country
                self.fields["postal_code"].initial = user_address.postal_code
    
    
    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            user_account, created = BankAccountPersonal.objects.get_or_create(user=user)
            user_address, created = BankAccountAddress.objects.get_or_create(user=user)

            user_account.account_type = self.cleaned_data['account_type']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.gender = self.cleaned_data['gender']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.country = self.cleaned_data['country']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.save()

        return user


class UserProfileForm(forms.ModelForm):
        account_type = forms.ChoiceField(choices=ACCOUNT_TYPE, disabled=True)
        birth_date = forms.DateTimeField(widget=forms.DateInput(attrs={"type": "date"}), disabled=True)
        gender = forms.ChoiceField(choices=GENDER_TYPE, disabled=True)
        street_address = forms.CharField(max_length=50, disabled=True)
        city = forms.CharField(max_length=20, disabled=True)
        country = forms.CharField(max_length=20, disabled=True)
        postal_code = forms.CharField(max_length=10, disabled=True)

        class Meta:
            model = User
            fields = ["first_name", "last_name", "email"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field in self.fields:
                self.fields[field].widget.attrs.update(
                    {
                        "class": (
                            "appearance-none block w-full bg-gray-200 "
                            "text-gray-700 border border-gray-200 rounded "
                            "py-3 px-4 leading-tight focus:outline-none "
                            "focus:bg-white focus:border-gray-500"
                        )
                    }
                )

            if self.instance:
                try:
                    user_account = self.instance.account
                    user_address = self.instance.address
                except:
                    user_account = None
                    user_address = None

                if user_account:
                    self.fields["account_type"].initial = user_account.account_type
                    self.fields["birth_date"].initial = user_account.birth_date
                    self.fields["gender"].initial = user_account.gender
                    self.fields["street_address"].initial = user_address.street_address
                    self.fields["city"].initial = user_address.city
                    self.fields["country"].initial = user_address.country
                    self.fields["postal_code"].initial = user_address.postal_code
                
