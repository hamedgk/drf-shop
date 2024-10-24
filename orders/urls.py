from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderView

urlpatterns = [
   path('orders/', OrderView.as_view()),
   path('orders/<int:pk>/', OrderView.as_view()),
]
