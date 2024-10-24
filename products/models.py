from django.db import models 
from django.db.models import Model 

class Product(Model): 
        name  = models.CharField("name", max_length=50, null=False)
        price = models.IntegerField("price", null=False)
        unit  = models.CharField("unit", max_length=20, null=False)
        created_at = models.DateTimeField(auto_now_add=True, null=False)
        updated_at = models.DateTimeField(auto_now=True)