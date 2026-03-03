from django.contrib import admin

from tasks.models import JobTask


# Register your models here.

@admin.register(JobTask)
class JobTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title",)