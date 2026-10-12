from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path(
        "briefs/",
        views.my_briefs,
        name="my_briefs"
    ),

    path(
        "briefs/new/",
        views.create_brief,
        name="create_brief"
    ),

    path(
        "briefs/<int:brief_id>/edit/",
        views.edit_brief,
        name="edit_brief"
    ),

    path(
        "briefs/<int:brief_id>/reuse/",
        views.reuse_brief,
        name="reuse_brief"
    ),

    path(
        "briefs/<int:brief_id>/",
        views.brief_detail,
        name="brief_detail"
    ),

    path(
        "ltt/",
        views.ltt_dashboard,
        name="ltt_dashboard"
    ),

    path(
        "ltt/briefs/<int:brief_id>/",
        views.ltt_brief_detail,
        name="ltt_brief_detail"
    ),

    path(
        "ltt/export/",
        views.export_briefs,
        name="export_briefs"
    ),

    path(
        "academic/",
        views.academic_reviews,
        name="academic_reviews"
    ),

    path(
        "academic/<int:brief_id>/",
        views.academic_reviews,
        name="academic_review"
    ),

    path(
        "signup/",
        views.partner_signup,
        name="partner_signup"
    ),

    path(
        "login/",
        views.PartnerLoginView.as_view(),
        name="partner_login"
    ),

    path(
        "logout/",
        LogoutView.as_view(
            next_page="partner_login"
        ),
        name="partner_logout"
    ),
]