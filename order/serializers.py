from rest_framework import serializers
from .models import Order, OrderItem
from product.models import Product
from django.db.models import Avg
from account_custom.send_email import send_recommendation

class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'product_title')


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    user = serializers.ReadOnlyField(source='user.email')
    products = OrderItemSerializer(write_only=True, many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products')
        request = self.context['request']
        user = request.user
        total_sum = 0
        result = []
        for product in products:
            category = product['product'].category
            objects = Product.objects.filter(category=category)

            rating = 0
            res = None
            for i in objects:
                if i.reviews.aggregate(Avg('rating'))['rating__avg'] > rating:
                    rating = i.reviews.aggregate(Avg('rating'))['rating__avg']
                    res = i
            result.append(res)
        send_recommendation(user, products, result)
        for product in products:
            try:
                total_sum += product['quantity'] * product['product'].price
            except KeyError:
                total_sum += product['product'].price

        order = Order.objects.create(user=user, total_sum=total_sum, status='open', **validated_data)
        for product in products:
            try:
                OrderItem.objects.create(order=order, product=product['product'], quantity=product['quantity'])
            except KeyError:
                OrderItem.objects.create(order=order, product=product['product'])
        return order

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['products'] = OrderItemSerializer(instance.items.all(), many=True).data
        repr.pop('product')
        return repr










