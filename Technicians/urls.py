from django.urls import path
from .views import *


app_name = 'Technicians'
urlpatterns = [
    path('List/', TechnicianList.as_view(), name='TechnicianList'),
    path('Trash/', TechnicianTrashList.as_view(), name='TechnicianTrashList'),
    path('Create/', TechnicianCreate.as_view(), name='TechnicianCreate'),
    path('Update/<int:pk>/', TechnicianUpdate.as_view(), name='TechnicianUpdate'),
    path('Delete/<int:pk>/', TechnicianDelete.as_view(), name='TechnicianDelete'),
]