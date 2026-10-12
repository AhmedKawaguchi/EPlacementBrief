from django.contrib import admin

from .models import Discipline, Duty, PlacementBrief, Review


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "active",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "name",
    )


@admin.register(Duty)
class DutyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "discipline",
        "active",
    )

    list_filter = (
        "discipline",
        "active",
    )

    search_fields = (
        "name",
    )


@admin.register(PlacementBrief)
class PlacementBriefAdmin(admin.ModelAdmin):
    list_display = (
        "position_title",
        "organisation_name",
        "status",
        "submitted_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "position_title",
        "organisation_name",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "brief",
        "reviewer",
        "outcome",
        "created_at",
    )

    list_filter = (
        "outcome",
    )