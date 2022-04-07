from rest_framework import serializers
from ecommerce.models import OrderMaster, OrderDetail


class OrderMasterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMaster
        fields = ['id', 'restaurant_id', 'customer_id', 'delivery_staff_id', 'delivered_date', 'delivered_time', 'delivery_cost']


class OrderDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['id', 'product_id', 'product_type_id', 'quantity', 'comment']
