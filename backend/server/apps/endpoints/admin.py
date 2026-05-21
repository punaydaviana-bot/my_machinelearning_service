from django.contrib import admin

from .models import ABTest, Endpoint, MLAlgorithm, MLAlgorithmStatus, MLRequest


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "owner")


@admin.register(MLAlgorithm)
class MLAlgorithmAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "owner", "parent_endpoint", "created_at")
    list_filter = ("parent_endpoint",)
    search_fields = ("name", "owner", "version")


@admin.register(MLAlgorithmStatus)
class MLAlgorithmStatusAdmin(admin.ModelAdmin):
    list_display = ("status", "active", "created_by", "parent_mlalgorithm", "created_at")
    list_filter = ("status", "active")


@admin.register(MLRequest)
class MLRequestAdmin(admin.ModelAdmin):
    list_display = ("response", "feedback", "parent_mlalgorithm", "created_at")
    list_filter = ("parent_mlalgorithm",)


@admin.register(ABTest)
class ABTestAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at", "ended_at")
    search_fields = ("title", "created_by")
