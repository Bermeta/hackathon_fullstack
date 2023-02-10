
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions


from .models import Product
from . import serializers
from .permissions import IsAuthorOrAdminOrPostOwner


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthorOrAdminOrPostOwner()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]