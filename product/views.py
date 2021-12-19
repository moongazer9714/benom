from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from service.general.permission import get_custom_permissions
from utils.serializers import  get_serializer_by_action
from .serializers import ProductSerializer, ProductCreateSerializer
from .models import Product

# Create your views here.

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
    
    def get_permissions(self):
        self.permission_classes = get_custom_permissions(request=self.request)
        return super(ProductViewSet, self).get_permissions()

    def get_serializer_class(self):
        return get_serializer_by_action(
            action=self.action,
            serializer = {
                'list': ProductSerializer,
                'retrieve': ProductSerializer,
                'create': ProductCreateSerializer,
                'update': ProductCreateSerializer,
                'partial_update': ProductCreateSerializer,
                'metadata': ProductSerializer,
            }
        )
    