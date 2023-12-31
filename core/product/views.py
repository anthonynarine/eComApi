from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer


# for documentation visit  https://www.django-rest-framework.org/api-guide/viewsets/#viewsets
class CategoryViewSet(viewsets.ViewSet):
    """A simple Viewset for viewing all categories"""

    queryset = Category.objects.all()
    # collect data from database

    # this decorator tells drf_specatcular which serializer we are using
    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        # pass collected data to be serializer
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """A simple Viewset for viewing all Brands"""

    queryset = Brand.objects.all()

    # collect data from database

    # this decorator tells drf_specatcular which serializer we are using
    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        # pass collected data to be serializer
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """A simple Viewset for viewing all Products"""

    # isacitve method called on all objects (see the product model manager)
    queryset = Product.objects.all().isactive()
    lookup_field = "slug"
    # default lookup field is pk

    def retrieve(self, request, slug=None):
        """function that bring in a individual product"""
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug).select_related("category", "brand"),
            many=True,
        )  # select_related() helps to make querying data more efficient. see notes below.

        return Response(serializer.data)

    # collect data from database
    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        # pass collected data to be serializer
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        # see NOTE below that explains this regex expression
        url_path=r"category/(?P<slug>[\w-]+)",
    )
    def list_product_by_category_slug(self, request, slug=None):
        """An endpoint to return product by category"""
        serializer = ProductSerializer(
            self.queryset.filter(category__slug=slug), many=True
        )
        return Response(serializer.data)

    """the regex expression above is to produce
    this url path - /api/product/category/{slug}/
    this path essentially expects and input term that matches a category name.
    see schema/docs path. our filter will traverse the products category field
    go to categories (which is a fk) we do not want the fk data so we traverse to name
    and if the name matches the inputed inpurt term is will return the data
    """


###############################NOTES#######################################

# NOTE select_related()
"""selected_related() - returns a QuerySet that will follow fk relationships,
selecting additional related-object data when it executes its query. This is
a performance booster which results in a single more complex query but means
later use of fk relationship wont require db queries. since our product comes 
with additional data from the category + brand and  tables
we can use select_related() to join the qurey using the fk eliminating
multiple individual queries it does not work. It does NOT work on reverse
fk relationships so we will not be able to include product line"""
