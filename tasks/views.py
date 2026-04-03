from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        user = User.objects.first()  # temporary until auth is added
        serializer.save(user=user)


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRunView(APIView):
    def post(self, request, pk, *args, **kwargs):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        task.status = "queued"
        task.save()

        return Response(
            {"message": "Task queued successfully"},
            status=status.HTTP_200_OK,
        )