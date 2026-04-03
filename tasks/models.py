from django.db import models
from django.contrib.auth.models import User

from candidates.models import Candidate


class Task(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('queued', 'Queued'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    job_description = models.TextField()
    key_requirements = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskCandidate(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    relevance_score = models.FloatField()
    relevance_label = models.CharField(max_length=20)

    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)

    explanation = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'candidate')

    def __str__(self):
        return f"{self.task.title} - {self.candidate.full_name} ({self.relevance_score})"