from django.shortcuts import render
from django.views.generic import DetailView, View, ListView
from .models import Books, RentalBooks, BorrowBooks
from account.models import PersonalAccount
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.contrib import messages

# Create your views here.


class BooksDetailViews(DetailView):
    model = Books
    template_name = 'books_detail.html'
    context_object_name = 'book'



class MyBooksView(LoginRequiredMixin, ListView):
    model = BorrowBooks
    template_name = 'my_books.html'
    context_object_name = 'borrow_records'

    def get_queryset(self):
        return BorrowBooks.objects.filter(user=self.request.user)





class ConfirmOderViews(LoginRequiredMixin,View):
    
    def post(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Books, pk= pk)
        email = request.POST.get('email')
        quantity = 1
        rental_days = int(request.POST.get('rental_days', 7))

        personal_account = get_object_or_404(PersonalAccount, user=request.user)

        RentalBooks.objects.create(
            user=request.user,
            book=book,
            rental_days=rental_days
        )

        if personal_account.points >= book.books_price:
            personal_account.points -= book.books_price
            personal_account.save()

            book.books_quantity -= quantity
            book.save()

            messages.success(request, f'Order for {book.books_title} confirmed!')
            return redirect(reverse('my_books'))
        
        else:
            messages.error(request, 'You do not have enough points to borrow this book.')
            return redirect(reverse('books_detail', args=[pk]))





class ReturnBookView(LoginRequiredMixin,View):
    def post(self,request, pk, *args, **kwargs):
        rental_books = get_object_or_404(RentalBooks, pk=pk,user=request.user)

        if rental_books.is_late:
            late_days = (timezone.now() - rental_books.due_date).days
            penalty_points = late_days * 10
            request.user.personal_account.points -= penalty_points
            request.user.personal_account.save()
        
        
        # Return the book
        rental_books.return_date = timezone.now()
        rental_books.save()
        
        # Add back the points
        book = rental_books.book
        request.user.personal_account.points += book.price
        request.user.personal_account.save()

        messages.success(request, f'Book returned. Points have been adjusted.')
        return redirect('profile')