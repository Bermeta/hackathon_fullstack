from rest_framework import serializers

from product.models import Product
from rating.serializers import ReviewActionSerializer


class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Product
        fields = ('owner', 'owner_email', 'title', 'price', 'preview', 'stock', 'sex')
        
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr


class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    reviews = ReviewActionSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def get_stars(instance):
        stars = {'5': instance.reviews.filter(rating=5).count(), '4': instance.reviews.filter(rating=4).count(),
                 '3': instance.reviews.filter(rating=3).count(), '2': instance.reviews.filter(rating=2).count(),
                 '1': instance.reviews.filter(rating=1).count()}
        return stars

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))
        rating = repr['rating']
        rating['ratings_count'] = instance.reviews.count()
        repr['stars'] = self.get_stars(instance)
        return repr

