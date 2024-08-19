from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import redirect
from .models import Car, Comment, Order
from .forms import CommentForm
from brands.models import Brand
from . import forms
from django.views import View

# Create your views here.

# Car details class


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        car = self.get_object()

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = car
            new_comment.save()
            return redirect('car_detail', pk=car.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        comments = car.comments.all()
        comment_form = forms.CommentForm()

        context['comments'] = comments
        context['comment_form'] = comment_form
        return context


# Car confirmation class
class ConfirmOrderView(View):

    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        form = forms.OrderForm(initial={'car_quantity': 1})
        return render(request, 'car_confirmorder.html', {'car': car, 'form': form})

    def post(self, request, pk):
        car = Car.objects.get(pk=pk)
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if car.car_quantity >= quantity:
                Order.objects.create(
                    user=request.user,
                    car=car,
                    quantity=quantity
                )
                car.car_quantity -= quantity
                car.save()
                return redirect('profile')
            else:
                form.add_error('quantity', 'Not enough cars in stock.')
        return render(request, 'car_confirmorder.html', {'car': car, 'form': form})
