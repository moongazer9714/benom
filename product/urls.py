from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()

router.register('product', ProductViewSet)

urlpatterns = router.urls