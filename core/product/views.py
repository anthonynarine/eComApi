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

    queryset = Product.objects.all()

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
        url_path=r"category/(?P<cat_name>\w+)/all",
        url_name="all",
    )
    def list_product_by_category(self, request, cat_name=None):
        """An endpoint to return product by category"""
        serializer = ProductSerializer(
            self.queryset.filter(category__name=cat_name), many=True
        )
        return Response(serializer.data)

    """the regex expression above is to produce
    this url path - /api/product/category/{cat_name}/all/
    this path essentially expects and input term that matches a category name.
    see schema/docs path. our filter will traverse the products category field
    go to categories (which is a fk) we do not want the fk data so we traverse to name
    and if the name matches the inputed inpurt term is will return the data
    """
