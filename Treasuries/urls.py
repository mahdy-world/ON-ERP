from .views import *
from django.urls import path

app_name = 'Treasuries'
urlpatterns = [
    

    path('treasuries/', TreasuryList.as_view(), name='TreasuryList'),
    path('treasuries/new/', TreasuryCreate.as_view(), name='TreasuryCreate'),
    path('treasuries/trash/', TreasuryTrashList.as_view(), name='TreasuryTrashList'),
    path('treasuries/<int:pk>/edit/', TreasuryUpdate.as_view(), name='TreasuryUpdate'),
    path('treasuries/<int:pk>/delete/', TreasuryDelete.as_view(), name='TreasuryDelete'),

    ####################
    path('payment/', PaymentMachinesList.as_view(), name='PaymentMachinesList'),
    path('payment/new/', PaymentMachinesCreate.as_view(), name='PaymentMachinesCreate'),
    path('payment/trash/', PaymentMachinesTrashList.as_view(), name='PaymentMachinesTrashList'),
    path('payment/<int:pk>/edit/', PaymentMachinesUpdate.as_view(), name='PaymentMachinesUpdate'),
    path('payment/<int:pk>/delete/', PaymentMachinesDelete.as_view(), name='PaymentMachinesDelete'),
    ]