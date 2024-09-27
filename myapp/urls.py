from django.urls import path
from .views import *

urlpatterns = [
    path('todo/', TodoView.as_view(), name = "list"),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('list-task/', ListTasksView.as_view(), name = 'list-task'),
    path('create-task/', CreateTaskView.as_view(), name = 'create-task'),
    path('update-task/<int:pk>/', UpdateTaskView.as_view(), name = 'update-task'),
]