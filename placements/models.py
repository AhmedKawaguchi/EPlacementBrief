from django.db import models
from django.contrib.auth.models import User


class Discipline(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Duty(models.Model):
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.PROTECT,
        related_name="duties"
    )

    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


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
        ("submitted", "Waiting for approval"),
        ("approved", "Approved"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    organisation_name = models.CharField(
        max_length=100
    )

    contact_name = models.CharField(
        max_length=50
    )

    contact_email = models.EmailField()

    position_title = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    position_description = models.TextField()

    number_of_positions = models.PositiveIntegerField(
        default=1
    )

    disciplines = models.ManyToManyField(
        Discipline,
        blank=True,
        related_name="placement_briefs"
    )

    duties = models.ManyToManyField(
        Duty,
        blank=True,
        related_name="placement_briefs"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.position_title} - "
            f"{self.organisation_name}"
        )


class Review(models.Model):
    OUTCOME_CHOICES = [
        ("approved", "Approved"),
    ]

    brief = models.ForeignKey(
        PlacementBrief,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="placement_reviews"
    )

    outcome = models.CharField(
        max_length=20,
        choices=OUTCOME_CHOICES,
        default="approved"
    )

    comments = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.get_outcome_display()} - "
            f"{self.brief.position_title}"
        )