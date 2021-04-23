from .views import *
from django.urls import path

app_name = 'Customers'
urlpatterns = [
    path('categories/', CategoryList.as_view(), name='CategoryList'),
    path('categories/new/', CategoryCreate.as_view(), name='CategoryCreate'),
    path('categories/trash/', CategoryTrashList.as_view(), name='CategoryTrashList'),
    path('categories/<int:pk>/edit/', CategoryUpdate.as_view(), name='CategoryUpdate'),
    path('categories/<int:pk>/delete/', CategoryDelete.as_view(), name='CategoryDelete'),
    
    
    path('customers/', CustomerList.as_view(), name='CustomerList'),
    path('customers/new/', customer_create , name='CustomerCreate'),
    path('customers/trash/', CustomerTrashList.as_view(), name='CustomerTrashList'),
    path('customers/<int:pk>/edit/', CustomerUpdate.as_view(), name='CustomerUpdate'),
    path('customers/<int:pk>/delete/', CustomerDelete.as_view(), name='CustomerDelete'),
    path('customers/<int:pk>/view/', CustomerDetail.as_view(), name='CustomerDetail'),
    path('customers/<int:pk>/invoices/', CustomerInvoices.as_view(), name='CustomerInvoices'),
    path('customers/<int:pk>/calls/', CustomerCalls.as_view(), name='CustomerCalls'),


    path('customers_type/', CustomerTypeList.as_view(), name='CustomerTypeList'),
    path('customers_type/new/', CustomerTypeCreate.as_view(), name='CustomerTypeCreate'),
    path('customers_type/trash/', CustomerTypeTrashList.as_view(), name='CustomerTypeTrashList'),
    path('customers_type/<int:pk>/edit/', CustomerTypeUpdate.as_view(), name='CustomerTypeUpdate'),
    path('customers_type/<int:pk>/delete/', CustomerTypeDelete.as_view(), name='CustomerTypeDelete'),
    
   
    


    path('customers/<int:pk>/calls/add/', add_call, name='add_call'),
    path('customers/calls/<int:pk>/view/', CallDetail.as_view(), name='CallDetail'),

    path('call_reasons/', CallReasonList.as_view(), name='CallReasonList'),
    path('call_reasons/new/', CallReasonCreate.as_view(), name='CallReasonCreate'),
    path('call_reasons/trash/', CallReasonTrashList.as_view(), name='CallReasonTrashList'),
    path('call_reasons/<int:pk>/edit/', CallReasonUpdate.as_view(), name='CallReasonUpdate'),
    path('call_reasons/<int:pk>/delete/', CallReasonDelete.as_view(), name='CallReasonDelete'),
    
    
    path('API/Customers/List/', CustomerAPIList.as_view(), name='CustomerAPIList'),
    path('API/Customers/<int:pk>/', CustomerAPIDetail.as_view(), name='CustomerAPIDetail'),
    ]