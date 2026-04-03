from django.urls import path
from .views import TaskListCreateView, TaskDetailView, TaskRunView

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("<int:pk>/run/", TaskRunView.as_view(), name="task-run"),
]