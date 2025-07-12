from django.shortcuts import redirect, render

from cart.models import Cart, CartItem
from store.models import Product, Variation


# Create your views here.
def _cart_id(request):
    """
    Function to get the cart ID from the session.
    If it doesn't exist, create a new one.
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    """
    View to add a product to the shopping cart.
    """
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == "POST":
        for key in request.POST:
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                )
                product_variation.append(variation)
                print(f"Variation found: {variation}")
            except Variation.DoesNotExist:
                pass

    # Get or create cart
    cart_id = _cart_id(request)
    cart, created = Cart.objects.get_or_create(cart_id=cart_id)

    # Check for existing cart items with this product
    cart_items = CartItem.objects.filter(product=product, cart=cart)
    existing_variations_list = []
    item_ids = []

    for item in cart_items:
        existing_variations = list(item.variation.all())
        existing_variations_list.append(existing_variations)
        item_ids.append(item.id)

    if product_variation in existing_variations_list:
        index = existing_variations_list.index(product_variation)
        item = CartItem.objects.get(id=item_ids[index])
        item.quantity += 1
        item.save()
    else:
        new_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            is_active=True,
        )
        if product_variation:
            new_item.variation.add(product_variation)
        new_item.save()

    return redirect("cart")


def remove_from_cart(request, product_id, cart_item_id):
    """
    View to remove a product from the shopping cart.
    """
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect("cart")


def remove_cart_item(request, cart_item_id):
    """
    View to remove a specific cart item from the shopping cart.
    """
    try:
        cart_item = CartItem.objects.get(
            id=cart_item_id, cart__cart_id=_cart_id(request)
        )
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect("cart")


def cart(request, total=0, quantity=0, cart_items=None):
    """
    View to display the shopping cart.
    """
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity
        tax = (total * 10) / 100  # Assuming a tax rate of 10%
        grand_total = total + tax
    except Cart.DoesNotExist:
        pass
    context = {
        "cart_items": cart_items,
        "total": total,
        "quantity": quantity,
        "tax": tax,
        "grand_total": grand_total,
    }

    return render(request, "store/cart.html", context)
