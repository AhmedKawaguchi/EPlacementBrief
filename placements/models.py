from django.db import models


class PlacementBrief(models.Model):
    company_name = models.CharField(max_length=200)
    position_title = models.CharField(max_length=200)