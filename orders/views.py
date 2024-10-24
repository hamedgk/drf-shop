from .models import Order, OrderProduct
from products.models import Product
from .serializers import OrderCreationSerializer, OrderRetrievalSerializer

from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class OrderView(APIView):
    serializer_class = OrderCreationSerializer
    permission_classes = [IsAuthenticated]

    def get_order(self, request, order_id):
        try:
            order_obj = Order.objects.get(pk=order_id)
            message = 'you do not have permission to access this object.'
            if order_obj.user != request.user:
                self.permission_denied(request, message=message)
        except Order.DoesNotExist:
            raise NotFound("order not found.")
        return order_obj

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        objects = Order.objects.filter(user=self.request.user)
        # serializer = OrderFlatSerializer(objects, many=True)
        serializer = OrderRetrievalSerializer(objects, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        order_id = kwargs['pk']
        order_obj = self.get_order(request, order_id)
        # serializer = OrderThroughSerializer(order_obj)
        serializer = OrderRetrievalSerializer(order_obj)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        serializer = OrderCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        data = serializer.validated_data
        order_id = kwargs['pk']
        order_obj = self.get_order(request, order_id)
        product_objects = [product_object['product'] for product_object in data['products']]
        order_obj.products.remove(*product_objects)
        serializer = OrderRetrievalSerializer(order_obj)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        data = serializer.validated_data
        order_obj = Order.objects.create(user=request.user)
        for through in data['products']:
            product_obj = through['product']
            quantity = through.get('quantity', 1)
            try:
                order_obj.products.add(product_obj, through_defaults={'quantity' : quantity})
            except Exception as e:
                return Response(str(e))

        order_obj.save()
        serializer = OrderRetrievalSerializer(order_obj)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = OrderCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        data = serializer.validated_data
        order_id = kwargs['pk']
        order_obj = self.get_order(request, order_id)
        order_obj.status = data['status']
        order_obj.save()
        for through in data['products']:
            product_obj = through['product']
            quantity = through.get('quantity', 1)
            try:
                order_obj.products.add(product_obj, through_defaults={'quantity' : quantity})
            except Exception as e:
                return Response(str(e))

        serializer = OrderRetrievalSerializer(order_obj)
        return Response(serializer.data)