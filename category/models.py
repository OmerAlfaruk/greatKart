from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, max_length=255, null=True)
    cat_image = models.ImageField(upload_to="photos/categories", blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_url(self):
        """
        Returns the URL for the category.
        This method is used to generate the URL for the category in templates.
        """
        return reverse("products_by_category", args=[self.slug])

    def __str__(self):
        return self.category_name
