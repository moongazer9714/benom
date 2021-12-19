from typing import Dict
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ParseError
from accounts.models import *

User = get_user_model

_USER_TYPES = {
    'seller': (Seller, SellerMore),
    'customer': (Customer, CustomerMore),
    'driver': (Driver, DriverMore),
}

def create_user_by_type(**validated_data:Dict)->User:
    user_type = validated_data.pop('type')
    if user_type.lower() == "admin":
        return _create_admin(
            user_model = Admin,
            user_more = AdminMore,
            **validated_data
        )
    if user_type.lower() == "moderator":
        return _create_moderator(
            user_model = Moderator,
            user_more = ModeratorMore,
            *validated_data
        )
    for user_type_key, user_objects in _USER_TYPES.items():
        UserModel, UserMoreModel = user_objects
        if user_type.lower() == user_type_key:
            return _create_user(
                user_model = UserModel,
                user_more = UserMoreModel,
                **validated_data
            )

def _create_user(user_model, user_more, **validated_data):
    try:
        user = user_model.objects.create_user(**validated_data)
        user_more.objects.create(user=user)
        return user
    except Exception:
        raise ParseError("Error while creating user.")
        
def _create_moderator(user_model, user_more, **validated_data):
    try:
        validated_data['is_staff']=True
        user = user_model.objects.create_user(**validated_data)
        user_more.objects.create(user=user)
        return user
    except Exception:
        raise ParseError("Error while creating moderator.")
    
def _create_admin(user_model, user_more, **validated_data):
    try:
        user = user_model.objects.create_superuser(**validated_data)
        user_more.objects.create(user=user)
        return user
    except Exception:
        raise ParseError("Error while creating admin.")

def create_user_by_validated_data(user:User, user_more=None, **validated_data:Dict)->User:
    if not user_more:
        return user.objects.create_user(**validated_data)
    extra_fields, validated_data = retrieve_extra_fields(**validated_data)
    user = user.objects.create_user(**validated_data)
    user_more.objects.create(user=user, **extra_fields)
    return user

def retrieve_extra_fields(**validated_data):
    extra_fields = validated_data.pop('more')
    return extra_fields, validated_data
    

