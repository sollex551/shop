from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('product_detail/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),

]
