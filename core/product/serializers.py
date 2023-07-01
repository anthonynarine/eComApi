from rest_framework import serializers
from .models import Brand, Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    """this tell django that brand+category has a relationship with product in order to make
    that connection we need to bring in their model's serializers. see the model for 
    how fk relationship was built. querying products will also need cat + brand since they 
    connected
"""

    class Meta:
        model = Product
        fields = "__all__"
