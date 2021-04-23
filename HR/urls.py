from .views import *
from django.urls import path

app_name = 'HR'
urlpatterns = [
    path('employees/', EmployeeList.as_view(), name='EmployeeList'),
    path('employees/new/', EmployeeCreate.as_view(), name='EmployeeCreate'),
    path('employees/<int:pk>/edit/', EmployeeUpdate.as_view(), name='EmployeeUpdate'),
    path('employees/<int:pk>/delete/', EmployeeDelete.as_view(), name='EmployeeDelete'),
    path('employees/<int:pk>/view/', EmployeeDetail.as_view(), name='EmployeeDetail'),
    path('employees/<int:pk>/upload/', UploadFile.as_view(), name='UploadFile'),
    path('employees/files/view/<int:pk>/', ViewFile.as_view(), name='ViewFile'),

    ]