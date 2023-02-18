from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from .models import Product, Favorites, Like
from . import serializers
from .permissions import IsAuthorOrAdminOrPostOwner, IsAuthor
from rest_framework import permissions, generics, response
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rating.serializers import ReviewActionSerializer, ReviewImages
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs/product.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class StandartResultPagination(PageNumberPagination):
    page_size = 9
    page_query_param = 'page'


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title', 'brand', 'sex')
    filterset_fields = ('sex', 'title', 'brand')

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

    @action(['GET'], detail=True)
    def get_favorites(self, request, pk):
        product = self.get_object()
        favorites = product.favorites.all()
        serializer = serializers.FavoritePostsSerializer(instance=favorites, many=True)
        return Response(serializer.data, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def favorites(self, request, pk):
        product = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.favorites.filter(product=product).exists():
                logger.error('This product already in favorites!')
                return Response('This product is already in favorites!',
                                status=400)
            Favorites.objects.create(owner=user, product=product)
            return Response('Added to favorites!', status=201)
        else:
            if user.favorites.filter(product=product).exists():
                user.favorites.filter(product=product).delete()
                return Response('Deleted from favorites!', status=204)
            logger.info('Request for unreal post!')
            logger.error('Product not found!')
            return Response('Product is not found!', status=400)

    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        product = self.get_object()
        likes = product.likes.all()
        serializer = serializers.LikeSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def like(self, request, pk):
        product = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.liked_products.filter(product=product).exists():
                logger.error('This product is already liked!')
                return Response('This product is already liked!', status=400)
            Like.objects.create(owner=user, product=product)
            return Response('You liked the product!', status=201)
        else:
            if not user.liked_products.filter(product=product).exists():
                logger.error('You didn\'t liked this product!')
                return Response('You didn\'t liked this product!', status=400)
            user.liked_products.filter(product=product).delete()
            return Response('Your like is deleted!', status=204)

    @action(['POST', 'GET'], detail=True)
    def reviews(self, request, pk):
        product = self.get_object()
        if request.method == 'GET':
            reviews = (product.reviews.all())
            serializer = ReviewActionSerializer(reviews, many=True).data
            return response.Response(serializer, status=200)
        else:
            if product.reviews.filter(owner=request.user).exists():
                logger.error('You already reviewed this product!')
                return response.Response('You already reviewed this product!', status=400)
            data = request.data
            serializer = ReviewActionSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            review = serializer.save(owner=request.user, product=product)
            images_data = request.FILES.getlist('images')
            for image in images_data:
                ReviewImages.objects.create(image=image, review=review)
            return response.Response(serializer.data, status=201)

    @action(['DELETE'], detail=True)
    def review_delete(self, request, pk):
        product = self.get_object()  # Product.objects.get(id=pk)
        user = request.user
        if not product.reviews.filter(owner=user).exists():
            logger.error('You didn\'t reviewed this product!')
            return response.Response('You didn\'t reviewed this product!', status=400)
        review = product.reviews.get(owner=user)
        review.delete()
        return response.Response('Successfully deleted', status=204)


class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthor)
