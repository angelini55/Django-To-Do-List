from django.urls import path
from .views import ToDoListView, CreateTaskView, DeleteTaskView, UpdateTaskView, IndividualTaskView, CreateSubTaskView, UpdateSubTaskView, DeleteSubTaskView

urlpatterns = [
    path('<str:user>/', ToDoListView.as_view(), name="lista"),
    path('<str:user>/create', CreateTaskView.as_view(), name="create"),
    path('<str:user>/<int:pk>', IndividualTaskView.as_view(), name="detail"),
    path('<str:user>/<int:pk>/update', UpdateTaskView.as_view(), name="update"),
    path('<str:user>/<int:pk>/delete', DeleteTaskView.as_view(), name="delete"),
    path('<str:user>/<int:task_pk>/create-subtask', CreateSubTaskView.as_view(), name="sub-create"),
    path('<str:user>/<int:task_pk>/update-subtask/<int:pk>', UpdateSubTaskView.as_view(), name="sub-update"),
    path('<str:user>/<int:task_pk>/delete-subtask/<int:pk>', DeleteSubTaskView.as_view(), name="sub-delete")
]