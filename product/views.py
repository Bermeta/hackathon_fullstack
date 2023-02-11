from rest_framework.viewsets import ModelViewSet
from .models import Product
from . import serializers
from .permissions import IsAuthorOrAdminOrPostOwner, IsAuthor
from rest_framework import permissions, generics, response
from rest_framework.response import Response
from .models import Like
from rest_framework.decorators import action


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
        post = self.get_object()
        likes = post.likes.all()
        serializer = serializers.LikeSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    # ../api/v1/posts/id/like/
    @action(['POST', 'DELETE'], detail=True)
    def like(self, request, pk):
        post = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.liked_posts.filter(post=post).exists():
                return Response('This post is already liked!', status=400)
            Like.objects.create(owner=user, post=post)
            return Response('You liked the post!', status=201)
        else:
            if not user.liked_posts.filter(post=post).exists():
                return Response('You didn\'t liked this post!', status=400)
            user.liked_posts.filter(post=post).delete()
            return Response('Your like is deleted!', status=204)


class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthor)
