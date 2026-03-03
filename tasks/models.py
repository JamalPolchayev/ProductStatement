from django.db import models
from django.conf import settings
# Create your models here.

class JobTask(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        CANCELED = "canceled", "Canceled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=225)
    description = models.TextField()
    requirements = models.JSONField(blank=True, null=True)
    search_params = models.JSONField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    total_found = models.IntegerField(default=0)
    total_parsed = models.IntegerField(default=0)
    total_scored = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.status})"