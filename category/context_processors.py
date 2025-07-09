from category.models import Category


# This context processor provides the menu links for categories
# It retrieves all categories from the database and makes them available in the context
def menu_links(request):

    links = Category.objects.all()
    return {"links": links}
