from django.contrib import admin


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product_name",)}
    list_display = (
        "product_name",
        "price",
        "stock",
        "category",
        "product_image",
        "modified_date",
        "is_available",
    )
    search_fields = ("product_name", "slug")


from .models import Product

admin.site.register(Product, ProductAdmin)
