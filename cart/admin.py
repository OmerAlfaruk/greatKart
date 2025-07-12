from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "date_added")
    search_fields = ("cart_id",)
    list_filter = ("date_added",)


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product", "cart", "quantity", "is_active")
    search_fields = ("product_name",)
    list_filter = ("is_active",)


admin.site.register(CartItem, CartItemAdmin)
