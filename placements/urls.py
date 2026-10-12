from django.urls import path
from . import views

urlpatterns = [
    path("briefs/", views.my_briefs, name="my_briefs"),
    path("briefs/new/", views.create_brief, name="create_brief"),
    path("briefs/<int:brief_id>/edit/", views.edit_brief, name="edit_brief"),
    path("briefs/<int:brief_id>/reuse/", views.reuse_brief, name="reuse_brief"),
    path("briefs/<int:brief_id>/", views.brief_detail, name="brief_detail"),
    path("signup/", views.partner_signup, name="partner_signup"),
    path("login/", views.PartnerLoginView.as_view(), name="partner_login"),
]