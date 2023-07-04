from rest_framework import serializers

from .models import Brand, Category, Product, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        # fields = "__all__"
        exclude = ["id"]


class ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLine
        # fields = "__all__"
        exclude = ["id", "is_active", "product"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")
    """ brand.name + category.name is accesed on serializers.CharField 
    (not BrandSerializer or CategorySerializer) since we only wnat to
    display that specific field to be displayed in our product data"""
    brand_name = serializers.CharField(source="brand.name")
    product_line = ProductLineSerializer(many=True)
    """this tells django that brand, category and productline
    (productlone has a reverse relationship)
    has a relationship with product in order to make that connection
    we need to bringin their model's serializers. see the model for 
    how fk relationship was built. querying products will also need 
    cat + brand since they're connected
    """

    class Meta:
        model = Product
        # fields = "__all__"
        fields = [
            "name",
            "slug",
            "description",
            "brand_name",
            "category_name",
            "product_line",
        ]
