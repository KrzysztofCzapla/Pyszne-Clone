from rest_framework import serializers
from main.models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'user', 'restaurant', 'delivery_address', 'FoodPackages','notes','total_price','created_at','orderStatus')