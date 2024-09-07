from django import forms
from .models import Transactions

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['amount','transaction_type']
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput(attrs={'class': 'hidden'})

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = 500
        amount = self.cleaned_data["amount"]
        
        if amount < min_deposit_amount:
            raise forms.ValidationError(f'You must provide a minimum amount at least {min_deposit_amount} taka')
        return amount
    
class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        mix_withdraw_amount = 20000
        balance = account.balance
        amount = self.cleaned_data.get('amount')

        if amount < min_withdraw_amount:
            raise forms.ValidationError(f'amount must be greater than {min_withdraw_amount} taka')
        
        if amount > mix_withdraw_amount:
            raise forms.ValidationError(f'amount must be greater than {mix_withdraw_amount} taka')
        
        if amount>balance:
            raise forms.ValidationError(f'insufficient balance, you have {balance} taka in your account')

        return amount
    
class LoanForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        balance = account.balance
        min_loan = 1000
        max_loan = (balance*3)
        amount = self.cleaned_data.get('amount')

        if amount < min_loan:
            raise forms.ValidationError(F'Amount must be greater than {min_loan}')
        
        if amount > max_loan:
            raise forms.ValidationError(F'Amount must be less than {max_loan}')
        
        return amount
    