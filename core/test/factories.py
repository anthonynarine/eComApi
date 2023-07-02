import factory

# bring in model for testing
from core.product.models import Brand, Category, Product


# build a factory to test the Category Model.
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # testing currently done on name field only
    name = "test_category"


# build a factory to test the Brand Model.
class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = "test_brand"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = "test_product"
    description = "test_descriptition"
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    """we're going to need to initiate a new brand and a new category in order 
    to associate and to build a product because of the referential integrity,
    because of the relationship that we have built in our database between the
    product table and the brand and category table.
    
    So what's going to happen here is that before we then generate this product,
    we're going to initiate and generate a brand, and then we do the same
    thing for the category as well.
    """
