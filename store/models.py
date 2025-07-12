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


class variationManager(models.Manager):
    def colors(self):
        return super(variationManager, self).filter(
            variation_category="color", is_active=True
        )

    def sizes(self):
        return super(variationManager, self).filter(
            variation_category="size", is_active=True
        )


variation_category_choices = (
    ("color", "color"),
    ("size", "size"),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choices
    )
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    objects = variationManager()

    def __str__(self):
        return f"{self.variation_category}: {self.variation_value} for {self.product.product_name}"
