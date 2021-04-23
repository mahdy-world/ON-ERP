
from django.urls import path
from .views import *

app_name = 'Tasks'
urlpatterns = [
    path('tasks/', TaskList.as_view() , name='TaskList'),
    path('tasks/trash/', TaskTrashListMain.as_view(), name='TaskTrashList'),
    path('tasks/done_list/', TaskListDone.as_view(), name='TaskListDone'),
    path('tasks/transfer/<int:pk>/', TaskTransfer.as_view(), name='TaskTransfer'),
    path('tasks/new/', TaskCreate.as_view(), name='TaskCreate'),
    path('tasks/view/<int:pk>/', TaskView.as_view(), name='TaskView'),
    path('tasks/edit/<int:pk>/', TaskUpdate.as_view(), name='TaskUpdate'),
    path('tasks/done/<int:pk>/', TaskDone.as_view(), name='TaskDone'),
    path('tasks/delete/<int:pk>/', TaskDelete.as_view(), name='TaskDelete'),
    
   
]
