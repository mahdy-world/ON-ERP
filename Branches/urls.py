from Branches.models import BranchWarehouses, Warehouse
from .views import *
from django.urls import path

app_name = 'Branches'
urlpatterns = [
    path('branches/', BranchList.as_view(), name='BranchList'),
    path('branches/new/', BranchCreate.as_view(), name='BranchCreate'),
    path('branches/trash/', BranchTrashList.as_view(), name='BranchTrashList'),
    path('branches/<int:pk>/edit/', BranchUpdate.as_view(), name='BranchUpdate'),
    path('branches/<int:pk>/delete/', BranchDelete.as_view(), name='BranchDelete'),


    path('branchwarehousescreate/<int:pk>/' , branch_warehouse_create, name='BranchWarehousesCreate'),


    path('warehouse/',WarehouseList.as_view(),name='WarehouseList' ),
    path('warehouse/new/', WarehouseCreate.as_view(), name='WarehouseCreate'),
    path('warehouse/trash/', WarehouseTrashList.as_view(), name='WarehouseTrashList'),
    path('Warehouse/<int:pk>/edit/', WarehouseUpdate.as_view(), name='WarehouseUpdate'),
    path('Warehouse/<int:pk>/delete/', WarehouseDelete.as_view(), name='WarehouseDelete'),

    
    ]