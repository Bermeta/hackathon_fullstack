from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
