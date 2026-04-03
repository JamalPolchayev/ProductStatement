from django.db import models

class Candidate(models.Model):
    full_name = models.CharField(max_length=255)
    linkedin_url = models.URLField(blank=True, null=True)

    current_position = models.CharField(max_length=255, blank=True, null=True)
    current_company = models.CharField(max_length=255, blank=True, null=True)

    total_experience_years = models.FloatField(blank=True, null=True)

    skills = models.JSONField(default=list)

    open_to_work = models.BooleanField(default=False)

    raw_profile_text = models.TextField(blank=True, null=True)

    source = models.CharField(max_length=100, default='linkedin')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name