from typing import Any
from django.shortcuts import render
from django.views.generic import DetailView, View, ListView, FormView
from .models import Books, RentalBooks, BorrowBooks
from account.models import PersonalAccount
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from .models import Coupon

# Create your views here.


class BooksDetailViews(DetailView):
    model = Books
    template_name = 'books_detail.html'
    context_object_name = 'book'



class ConfirmOderViews(LoginRequiredMixin, View):

     def post(self, request, pk, *args, **kwargs):

        book = get_object_or_404(Books, pk=pk)
        email = request.POST.get('email')
        quantity = 1
        rental_days = int(request.POST.get('rental_days', 7))
        
        personal_account = get_object_or_404(PersonalAccount, user=request.user)

        if personal_account.points >= book.books_price:
            if book.books_quantity >= quantity:
 
                BorrowBooks.objects.create(
                    user=request.user,
                    book=book,
                    email=email,
                    quantity=quantity,
                    rental_days=rental_days,
                    return_due_date=timezone.now() + timedelta(days=rental_days)  
                )

                personal_account.points -= book.books_price
                personal_account.save()

                book.books_quantity -= quantity
                book.save()

                messages.success(request, f'Order for "{book.books_title}" confirmed!')
                return redirect(reverse('my_books'))
            else:
                messages.error(request, 'Not enough books available.')
        else:
            messages.error(request, 'You do not have enough points to borrow this book.')
        
        return redirect(reverse('books_detail', args=[pk]))  


class ReturnBookView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        borrow_book = get_object_or_404(BorrowBooks, pk=pk, user=request.user)
        book = borrow_book.book
        
        # Access the user's personal account
        personal_account = get_object_or_404(PersonalAccount, user=request.user)
        
        if timezone.now() > borrow_book.return_due_date:
            late_days = (timezone.now() - borrow_book.return_due_date).days
            penalty_points = late_days * 10
            personal_account.points -= penalty_points
            personal_account.save()
        
        # Return the book
        borrow_book.returned_on = timezone.now()
        borrow_book.save()
        
        # Add back the points
        personal_account.points += book.books_price
        personal_account.save()

        book.books_quantity += 1
        book.save()

        messages.success(request, 'Book returned. Points have been adjusted.')
        return redirect('my_books')

          


class MyBooksView(LoginRequiredMixin, ListView):
    model = BorrowBooks
    template_name = 'my_books.html'
    context_object_name = 'borrow_records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'my_books'
        return context

    def get_queryset(self):

        queryset = BorrowBooks.objects.filter(user=self.request.user, returned_on__isnull=True)
        return queryset
    
class HistoryViews(ListView):
        model = BorrowBooks
        template_name = 'history.html'
        context_object_name = 'book'

        def get_context_data(self, **kwargs: Any):
            context =  super().get_context_data(**kwargs)
            context['active_page'] = 'history'
            user = self.request.user

            context['borrowed_books'] = BorrowBooks.objects.filter(user=user, returned_on__isnull=True).order_by('-borrowed_on')
            context['returned_books'] = BorrowBooks.objects.filter(user=user, returned_on__isnull=False).order_by('-returned_on')
            return context
        
class CouponView(ListView):
    model = Coupon
    template_name = 'coupon.html'
    context_object_name = 'coupons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'coupons'
        return context

class CouponConfirmView(FormView):
  
    def post(self, request, *args, **kwargs):
        coupon_id = self.kwargs['coupon_id']
        coupon = get_object_or_404(Coupon, id=coupon_id)
        user_account = PersonalAccount.objects.get(user=request.user)
        

        if user_account.points >= coupon.price:
            user_account.points += coupon.points
            user_account.save()
            messages.success(request, f'Coupon purchased successfully! {coupon.points} points added to your account.')
        else:
            messages.error(request, 'Insufficient points to purchase this coupon.')
        
        return redirect(reverse('coupons'))