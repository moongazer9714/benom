import traceback
from django.db import IntegrityError, transaction
from django.db.models import fields, manager
from djoser.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from rest_framework.serializers import raise_errors_on_nested_writes, ModelSerializer
from rest_framework.utils import model_meta
from address.serializers import SellerAddressSerializer, CustomerAddressSerializer
from service.accounts.general import create_user_by_type, create_user_by_validated_data, retrieve_extra_fields
from order.serializers import OrderDetailSerializers, CartDetailSerializer
from .models import *


class CustomModelSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        print(instance, validated_data)
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        extra_fields, validated_data = retrieve_extra_fields(**validated_data)
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)
        for attr, value in extra_fields.items():
            setattr(instance.more, attr, value)
        instance.save()
        instance.more.save()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.save(value)
        return instance


class CustomerMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMore
        exclude = ('id', 'user')


class CustomerSerializer(CustomModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='accounts:customer-detail')
    customer_address = CustomerAddressSerializer(many=True)
    customer_orders = OrderDetailSerializers(many=True)
    carts = CartDetailSerializer(many=True)
    more = CustomerMoreSerializer()
    
    class Meta:
        model = Customer
        fields = '__all__'
    
    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)
        return create_user_by_validated_data(Customer, CustomMore, **validated_data)

    def validate_type(self, value):
        if value != 'customer':
            raise serializers.ValidationError('Customer user must have type=customer')
        return value

    def validate_is_superuser(self, value):
        if value is True:
            raise serializers.ValidationError('Customer must not have is_superuser')
        return value


class SellerMoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SellerMore
        exclude = ('id', 'user')


class SellerSerializer(CustomModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='accounts:seller-detail')
    more = SellerMoreSerializer()
    seller_addresses = SellerAddressSerializer(many=True)
    products = serializers.SerializerMethodField('get_seller_products')

    class Meta:
        model = Seller
        fields = '__all__'

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)
        return create_user_by_validated_data(Seller, SellerMore, **validated_data)

    def validate_type(self, value):
        if value != 'seller':
            raise serializers.ValidationError('Seller user must have type=seller')
        return value

    def validate_is_superuser(self, value):
        if value is True:
            raise serializers.ValidationError('Seller must not have is_superuser=True')
        return value

    def get_seller_products(self, seller):
        if seller.products:
            return [product.id for product in seller.products.all()]

    def get_seller_address(self,seller):
        return [address.id for address in seller.seller_addresses.all()]


class ModeratorMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeratorMore
        exclude = ('id', 'user')


class ModeratorSerializer(CustomModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='accounts:moderator-detail')
    more = ModeratorMoreSerializer()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)
        return create_user_by_validated_data(Moderator, ModeratorMore, **validated_data)

    def validate_type(self, value):
        if value != 'moderator':
            raise serializers.ValidationError('Moderator must have type=moderator')
        return value
    
    def validate_is_staff(self, value):
        if value is True:
            raise serializers.ValidationError('Moderator must have is_staff=True')
        return value


class AdminMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminMore
        exclude = ('id', 'user')


class AdminSerializer(CustomModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='accounts:moderator-detail')
    more = AdminMoreSerializer()
    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)
        return create_user_by_validated_data(Admin, AdminMore, **validated_data)

    def validate_type(self, value):
        if value != 'admin':
            raise serializers.ValidationError('Admin user must have type=admin')
        return value
    
    def validate_is_superuser(self, value):
        if value is True:
            raise serializers.ValidationError('Admin must have is_superuser=True')
        return value


class CustomUserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='accounts:user-detail')
    class Meta:
        model = User
        fields = '__all__'


class CustomUserCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail('cannot_create_user')
        return user
    
    def perform_create(self, validated_data):
        with transaction.atomic():
            user = create_user_by_type(** validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=['is_active'])
        return user


    
