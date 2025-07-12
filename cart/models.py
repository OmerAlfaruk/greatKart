from django.db import models
from store.models import Product, Variation


# Create your models here.
class Cart(models.Model):
    """
    Model to represent a shopping cart.
    """

    cart_id = models.CharField(max_length=255, unique=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.cart_id} created on {self.date_added}"


class CartItem(models.Model):
    """
    Model to represent an item in the shopping cart.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        """
        Calculate the subtotal for this cart item.
        """
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} in cart {self.cart.cart_id}"
