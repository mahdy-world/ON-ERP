from django.urls import path
from .views import *


app_name = 'Website'
urlpatterns = [
    path('', HomePage.as_view(), name='HomePage'),
    path('shop/', Shop.as_view(), name='Shop'),
    path('<int:pk>/products/', ProductList.as_view(), name='ProductList'),
    path('product/<int:pk>/', ProductView.as_view(), name='ProductView'),
    path('add_to_cart/', AddToCart.as_view(), name='AddToCart'),
    path('search/', Search.as_view(), name='Search')
]