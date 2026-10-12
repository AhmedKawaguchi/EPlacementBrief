from django.urls import path
from . import views

urlpatterns = [
    path("briefs/new/", views.create_brief, name="create_brief"),
]