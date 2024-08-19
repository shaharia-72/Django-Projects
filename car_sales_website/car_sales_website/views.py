from cars.models import Car
from django.views.generic import ListView
from cars.models import Car
from brands.models import Brand
from django.shortcuts import render, redirect


class HomePage(ListView):
    template_name = 'home.html'
    model = Car
    context_object_name = 'cars'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        return context


def category(request, brand_id):
    brand = Brand.objects.filter(pk=brand_id).first()
    if brand is None:
        return redirect('home')
    cars = Car.objects.filter(brand=brand)
    brands = Brand.objects.all()
    return render(request, 'home.html', {'cars': cars, 'brands': brands})
