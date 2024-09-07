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
from django.db import transaction

class TransactionViewMix(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transactions_form.html'
    model = Transactions
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
        })
        return context

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
        account.save(update_fields=['balance'])
        messages.success(self.request, f'{amount} taka was successfully added to your account. Now you have {account.balance} taka.')
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
        account.save(update_fields=['balance'])
        messages.success(self.request, f'{amount} taka was successfully withdrawn. Now you have {account.balance} taka.')
        return super().form_valid(form)

class LoanRequestView(TransactionViewMix):
    form_class = LoanForm
    title = 'Loan Request'

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        current_loan_pending_count = Transactions.objects.filter(
            account=self.request.user.account,
            transaction_type=LOAN,
            loan_approved=True
        ).count()

        if current_loan_pending_count >= 3:
            return HttpResponse("You have exceeded your limit. Please wait for admin feedback.")
        
        messages.success(self.request, f'{amount} taka was successfully applied for a loan.')
        return super().form_valid(form)

class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transactions_report.html'
    model = Transactions
    balance = 0

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )

        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            queryset = queryset.filter(timestamp__gte=start_date, timestamp__lte=end_date)
        else:
            self.balance = self.request.user.account.balance

        return queryset.distinct()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Transaction Report',
            'balance': self.request.user.account.balance,
        })
        return context

class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transactions, id=loan_id)

        if loan.loan_approved:
            user_account = loan.account
            if loan.amount <= user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect('loan_list')
            else:
                messages.error(self.request, 'You don\'t have sufficient funds.')
        return redirect('loan_list')

class LoanListView(LoginRequiredMixin, ListView):
    model = Transactions
    template_name = 'transactions/loan_request.html'
    context_object_name = 'loans'

    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transactions.objects.filter(account=user_account, transaction_type=LOAN)
        # print(queryset)
        return queryset


@transaction.atomic
def approve_loan(request, loan_id):
    loan = get_object_or_404(Transactions, id=loan_id)
    if request.method == "POST":
        loan.loan_approved = True
        loan.save()

        user_account = loan.account
        user_account.balance += loan.amount
        user_account.save(update_fields=['balance'])
        messages.success(request, f'Loan of {loan.amount} taka approved. New balance is {user_account.balance} taka.')
        return redirect('loan_list')
