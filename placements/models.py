from django.db import models
from django.contrib.auth.models import User


# Defines the info stored by each placement brief
class PlacementBrief(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="placement_briefs",
        null=True,
        blank=True
    )

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("approved", "Approved"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    organisation_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=50)
    contact_email = models.EmailField()
    position_title = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)
    position_description = models.TextField()
    number_of_positions = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.position_title} - {self.organisation_name}"