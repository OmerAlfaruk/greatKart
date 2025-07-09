from django.shortcuts import get_object_or_404, render

from category.models import Category
from store.models import Product


# Create your views here.
def store(request, category_slug=None):
    """Render the store page with products and categories."""
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        produc_count = products.count()

    else:

        categories = Category.objects.all().filter()
        products = Product.objects.all().filter(is_available=True).order_by("id")
        produc_count = products.count()
    context = {
        "categories": categories,
        "products": products,
        "produc_count": produc_count,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    """Render the product detail page."""
    try:
        product = Product.objects.get(
            category__slug=category_slug, slug=product_slug, is_available=True
        )
    except Exception as e:
        raise e

    context = {
        "product": product,
    }
    return render(request, "store/product_detail.html", context)
