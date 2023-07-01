from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer


# for documentation visit  https://www.django-rest-framework.org/api-guide/viewsets/#viewsets
class CategoryViewSet(viewsets.ViewSet):
    """A simple Viewset for viewing all categories"""

    queryset = Category.objects.all()
    # collect data from database

    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        # pass collected data to be serializer
        return Response(serializer.data)
