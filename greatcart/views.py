from django.http import HttpResponse
from django.shortcuts import render

from store.models import Product


def home(request):
    products = Product.objects.all().filter(is_available=True).order_by("id")
    context = {
        "products": products,
    }
    return render(request, "index.html", context)
