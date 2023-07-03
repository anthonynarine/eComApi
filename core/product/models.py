from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class ActiveQueryset(models.QuerySet):
    """overiding the base queryset"""

    def isactive(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    # django-mptt install method used to create a fk
    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    # slug creates a usable url string that can be utilized as
    # a paramater instead of ID in the url which can then be passed to the view
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    # links products to brand via fk
    category = TreeForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )  # links products to category
    is_active = models.BooleanField(default=False)
    # is_active allows us to filter products that are only
    # active and we can toggle this functionality
    objects = ActiveQueryset().as_manager()  # overiding default query

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(
        decimal_places=2, max_digits=5
    )  # 5 digit max for prices
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    # on_delete of a product curently will also delete the product line
    # related_name was added to be used to establish a reverse relationship
    # with product for serialization. see serializer
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)

    ##############################NOTES######################
    #   NOTE  MANAGERS
    """manager is a class that provides a way to
    query the database for instances of a particular
    model. It acts as an interface between the model
    and the database, allowing you to perform various
    operations such as creating, retrieving, updating,
    and deleting model instances.
    
    This use case:
    Creating a custom manage for our model to add additonal
    customizations which can affect the queries that we run in 
    our application. Reason to do this - first - modify query sets that the
    manager returns and second  add come custom methods to a manager so that 
    we can access that extra functionality 
    
    We only want to return products whereby, for example, is active equals ture.
    so we create an override to the base query set and override the manager,get query set
    method, get_queryset,and use super; remember that is going to allow us to access methods
    of the base class and then provide overrides.nd that's essentially what we're doing 
    here So get query set, filter is active.  """
