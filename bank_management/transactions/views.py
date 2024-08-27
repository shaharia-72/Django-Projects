from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transactions
from .forms import DepositForm, WithdrawForm, LoanForm
from .constants import DEPOSIT, WITHDRAWAL, LOAN, LOAN_PAID
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

class TransactionViewMix(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transactions_form.html'
    model = Transactions
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs
        kwargs.update({
            'account': self.request.user.account,
        })
        return kwargs

    def get_context_data(self, **kwargs) :
        context =super().get_context_data(**kwargs)
        context.update({
            'title':self.title,
        })
        

class DepositMoneyView(TransactionViewMix):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        account = self.request.user.account
        account.balance += amount
        
        account.save(
            update_fields = ['balance']
        )
        
        messages.success(self.request, f'{amount} taka was added in your account, now you have {amount.balance} taka.')
        return super().form_valid(form)


class WithdrawMoneyView(TransactionViewMix):
    form_class = WithdrawForm
    title = 'Withdraw'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        account = self.request.user.account
        account.balance -= amount
        
        account.save(
            update_fields = ['balance']
        )
        
        messages.success(self.request, f'{amount} taka was succesfully withdraw, now you have {amount.balance} taka.')
        return super().form_valid(form)
    

class LoanRequestView(TransactionViewMix):
    form_class = LoanForm
    title = 'Loan Request'

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        
        current_loan_pending_count = Transactions.objects.filter( account = self.request.user.account, Transactions_type = 3, loan_approved = True).count()
        
        if current_loan_pending_count >= 3:
            return HttpResponse("you have over your limit, wait for admin feedback")
        
        messages.success(self.request, f'{amount} taka was succesfully applied for loan, now you have {amount.balance} taka.')
        return super().form_valid(form)
    

class TransactionReportView(LoginRequiredMixin,ListView):
    template_name = ''
    model = Transactions
    balance = 0

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account = self.request.user.account
        )

        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            queryset = queryset.filter(timestamp_date_gte = start_date, timestamp_date_lte = end_date, )

            return queryset.distinct()
        
    def get_context_data(self, **kwargs):      
            context =super().get_context_data(**kwargs)
            context.update({
                'title':self.request.user.account
            })
            return context


class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transactions, id=loan_id)

        if loan.loan_approved:
            user_account = loan.account
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect()
            else:
                messages.error(self.request, ' you dont have sufficient amount')
                return redirect()


class LoanListView(LoginRequiredMixin, ListView):
    model = Transactions
    template_name = ''
    context_object_name = 'Loans'

    def get_queryset(self):
        user_account = self.request.user.account
        querySet = Transactions.objects.filter(account = user_account, transition_type = LOAN)
        return querySet