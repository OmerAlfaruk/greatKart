from django.db import models
from django.urls import reverse


from category.models import Category


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, max_length=255, null=True)
    price = models.IntegerField()
    stock = models.IntegerField(default=0)
    product_image = models.ImageField(
        upload_to="photos/products", blank=True, null=True
    )
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_url(self):
        """
        Returns the URL for the product.
        This method is used to generate the URL for the product in templates.
        """
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
