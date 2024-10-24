from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Order, OrderProduct
from products.models import Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']
    
    def __init__(self, *args, **kwargs):
        self.Meta.depth = kwargs.pop('depth', 0)
        super().__init__(*args, **kwargs)

class OrderCreationSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user']
        depth = 1

class OrderRetrievalSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user']
        depth = 1

    def get_products(self, obj):
        qset = OrderProduct.objects.filter(order=obj)
        return [OrderProductSerializer(m, depth=1).data for m in qset]

# class OrderProductFlatSerializer(serializers.ModelSerializer):
#     id = serializers.ReadOnlyField(source='product.id')
#     name = serializers.ReadOnlyField(source='product.name')
#     price = serializers.ReadOnlyField(source='product.price')
#     unit = serializers.ReadOnlyField(source='product.unit')
#     class Meta:
#         model = OrderProduct
#         fields = ['id','name', 'price','unit', 'product', 'quantity']

# class OrderFlatSerializer(serializers.ModelSerializer):
#     products = OrderProductFlatSerializer(source='orderproduct_set', many=True)
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = Order
#         fields = '__all__'
#         read_only_fields = ['user']
#         depth = 1