
from django.db import models

# Defines the info stored by each document
class PlacementBrief(models.Model):
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