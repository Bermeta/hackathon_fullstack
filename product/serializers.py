from django.db.models import Avg
from rest_framework import serializers
from product.models import Product, Like, Favorites
from rating.serializers import ReviewActionSerializer
from rating.models import Review
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


class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Product
        fields = ('id', 'owner', 'owner_email', 'title', 'price', 'preview', 'stock', 'sex')
        
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr


class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    reviews = ReviewActionSerializer(many=True, read_only=True)
    stars = serializers.SerializerMethodField('get_ratings_detail')

    class Meta:
        model = Product
        fields = '__all__'

    def get_ratings_detail(self, obj):
        stars = Review.objects.filter(product=obj)

        from collections import Counter

        stars = Counter(stars.values_list("rating", flat=True))
        return stars

    # @staticmethod
    # def get_stars(instance):
    #     stars = {'5': instance.reviews.filter(rating=5).count(), '4': instance.reviews.filter(rating=4).count(),
    #              '3': instance.reviews.filter(rating=3).count(), '2': instance.reviews.filter(rating=2).count(),
    #              '1': instance.reviews.filter(rating=1).count()}
    #     return stars

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating_avg'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        # rating_avg = repr['rating_avg']
        # rating['ratings_count'] = instance.reviews.count()
        # repr['stars'] = self.get_stars(instance)
        return repr


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = '__all__'

    def validate_data(self, attrs):
        request = self.context['request']
        user = request.user
        product = attrs['product']
        if product.likes.filter(owner=user).exists():
            logger.error('You already liked this product')
            raise serializers.ValidationError('You already liked product!')
        return attrs


class LikedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = 'product'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product_title'] = instance.post.title
        preview = instance.post.preview
        repr['product_preview'] = preview.url

        return repr
        

class FavoritePostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('id', 'product')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product_title'] = instance.post.title
        preview = instance.post.preview
        repr['product_preview'] = preview.url
        return repr

