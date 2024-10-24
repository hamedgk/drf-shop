from django.contrib import admin
from products.models import Product
from orders.models import Order

admin.site.register(Product)
admin.site.register(Order)
