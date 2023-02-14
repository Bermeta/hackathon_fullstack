from rest_framework.viewsets import ModelViewSet
from . import serializers
from .permissions import IsAuthorOrAdminOrPostOwner, IsAuthor
from rest_framework import permissions, generics, response
from rest_framework.response import Response
from .models import Like, Product
from rest_framework.decorators import action
from rating.serializers import ReviewActionSerializer, ReviewImages


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

    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        product = self.get_object()
        likes = product.likes.all()
        serializer = serializers.LikeSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    # ../api/v1/posts/id/like/
    @action(['POST', 'DELETE'], detail=True)
    def like(self, request, pk):
        product = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.liked_posts.filter(product=product).exists():
                return Response('This product is already liked!', status=400)
            Like.objects.create(owner=user, product=product)
            return Response('You liked the product!', status=201)
        else:
            if not user.liked_posts.filter(post=post).exists():
                return Response('You didn\'t liked this product!', status=400)
            user.liked_posts.filter(product=product).delete()
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
            return response.Response('You didn\'t reviewed this product!', status=400)
        review = product.reviews.get(owner=user)
        review.delete()
        return response.Response('Successfully deleted', status=204)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductListSerializer


class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthor)

        
    