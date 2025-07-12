from django.shortcuts import get_object_or_404, render

from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category
from store.models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


# Create your views here.
def store(request, category_slug=None):
    """Render the store page with products and categories."""
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)  # Show 6 products per page
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        produc_count = products.count()

    else:

        categories = Category.objects.all().filter()
        products = Product.objects.all().filter(is_available=True).order_by("id")
        paginator = Paginator(products, 3)  # Show 6 products per page
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        produc_count = products.count()
    context = {
        "categories": categories,
        "products": paged_products,
        "produc_count": produc_count,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    """Render the product detail page."""
    try:
        product = Product.objects.get(
            category__slug=category_slug, slug=product_slug, is_available=True
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=product
        ).exists()
    except Exception as e:
        raise e

    context = {
        "product": product,
        "in_cart": in_cart,
    }
    return render(request, "store/product_detail.html", context)


def search(request):
    """Render the search results page."""
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword),
            )
            product_count = products.count()
        else:
            products = Product.objects.all().filter(is_available=True)
            product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        "products": products,
        "product_count": product_count,
    }
    return render(request, "store/store.html", context)
