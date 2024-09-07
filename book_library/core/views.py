from django.shortcuts import render
from django.views.generic import TemplateView
from books.models import Books
from books_categories.models import BooksCategory

# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Books.objects.all()  
        context['book_categories'] = BooksCategory.objects.all() 
        return context

    
