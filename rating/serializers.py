# from rest_framework import serializers
# from rating.models import Review
#
#
# class ReviewSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.email')
#
#     class Meta:
#         model = Review
#         fields = '__all__'
#
#     def validate(self, attrs):
#         product = attrs['product']
#         requests = self.context['request']
#         user = requests.user
#         if user.reviews.filter(product=product).exists():
#             raise serializers.ValidationError('You already reviewed this product!')
#         return attrs
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         review = Review.objects.create(**validated_data)
#         images_data = request.FILES.getlist('images')
#         for image in images_data:
#             ReviewImages.objects.create(image=image, review=review)
#         return review
#
#     def to_representation(self, instance):
#         repr = super().to_representation(instance)
#         repr['images'] = ReviewImageSerializer(instance.images.all(), many=True).data
#
#         return repr
#
#
# class ReviewUpdateSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.email')
#     product = serializers.ReadOnlyField(source='product.title')
#
#     class Meta:
#         model = Review
#         fields = '__all__'
#
#     def update(self, instance, validated_data):
#         request = self.context.get('request')
#         for k, v in validated_data.items():
#             setattr(instance, k, v)
#         instance.save()
#         instance.images.all().delete()
#         images_data = request.FILES.getlist('images')
#         for image in images_data:
#             ReviewImages.objects.create(image=image, review=instance)
#         return instance
