from django.db.models import fields
from rest_framework import serializers
from product.models import Product
from product.serializers import ProductSerializer
from service.category.serializers import FilterCategorySerializer
from service.general.serializers import RecurseiveSerializer
from .models import Category

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail', lookup_field="slug")
    children = RecurseiveSerializer(many=True)
    products = ProductSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCategorySerializer
        model = Category
        fields = ("id", "title", "description", "children", "products", "url")
        