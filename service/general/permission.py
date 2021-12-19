from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, BasePermission, AllowAny
from utils.permissions import IsOwnerOrAdmin, IsStaff
from utils.http_methods import METHODS
from utils.exceptions import BadHTTPMethodError

_DEFAULT_PERMISSIONS = {
    'GET':(AllowAny,),
    'POST':(AllowAny,),
    'PUT':(AllowAny,),
    'PATCH':(AllowAny,),
    'DELETE':(AllowAny,),
}

def get_custom_permissions(request, **extra_permissions):
    if extra_permissions:
        for method, permissions in extra_permissions.items():
            for permission in permissions:
                if not isinstance(permission, BasePermission):
                    raise TypeError(f"TypeError: unexpected type of permission '{permission}'")
                if  method not in METHODS:
                    raise BadHTTPMethodError(f"BadHTTPMethodError: unexpected HTTP method '{method}'")
                _DEFAULT_PERMISSIONS[method] = permissions
        permissions = (
            permission
            for method, permission in _DEFAULT_PERMISSIONS.items()
            for permission in permissions
            if request.method == method
        )
        return permissions
