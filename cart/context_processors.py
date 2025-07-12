from cart.views import _cart_id
from .models import CartItem, Cart


def counter(request):
    """
    Context processor to count the number of items in the cart.
    """
    if "admin" in request.path:
        return {}
    cart_count = 0
    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        cart_items = CartItem.objects.all().filter(cart=cart[:1], is_active=True)
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0

    return dict(cart_count=cart_count)
