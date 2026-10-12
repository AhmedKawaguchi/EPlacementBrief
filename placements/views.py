import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import EPlacementForm, PartnerLoginForm, PartnerSignupForm
from .models import Discipline, PlacementBrief, Review


def is_ltt(user):
    return (
        user.is_superuser
        or user.groups.filter(name="LTT").exists()
    )


def is_academic(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Academic").exists()
    )


@login_required(login_url="partner_login")
def create_brief(request):
    if request.method == "POST":
        form = EPlacementForm(request.POST)

        if form.is_valid():
            action = request.POST.get("action")

            if action == "submit":
                required_fields = [
                    "organisation_name",
                    "contact_name",
                    "contact_email",
                    "position_title",
                    "position_description",
                    "disciplines",
                    "duties",
                ]

                missing_fields = False

                for field in required_fields:
                    if not form.cleaned_data.get(field):
                        form.add_error(
                            field,
                            "This field is required before submitting."
                        )
                        missing_fields = True

                if missing_fields:
                    return render(
                        request,
                        "placements/brief_form.html",
                        {
                            "form": form,
                            "page_name": "Create Placement Brief",
                        }
                    )

            brief = form.save(commit=False)
            brief.owner = request.user

            if action == "submit":
                brief.status = "submitted"
                brief.submitted_at = timezone.now()

                message = (
                    "Placement Brief submitted and is "
                    "waiting for approval."
                )

            else:
                brief.status = "draft"
                message = "Draft saved successfully."

            brief.save()
            form.save_m2m()

            messages.success(
                request,
                message
            )

            return redirect("my_briefs")

    else:
        form = EPlacementForm()

    return render(
        request,
        "placements/brief_form.html",
        {
            "form": form,
            "page_name": "Create Placement Brief",
        }
    )


@login_required(login_url="partner_login")
def my_briefs(request):
    briefs = PlacementBrief.objects.filter(
        owner=request.user
    ).order_by(
        "-updated_at"
    )

    return render(
        request,
        "placements/my_briefs.html",
        {
            "briefs": briefs
        }
    )


@login_required(login_url="partner_login")
def brief_detail(request, brief_id):
    brief = get_object_or_404(
        PlacementBrief,
        id=brief_id,
        owner=request.user
    )

    return render(
        request,
        "placements/brief_info.html",
        {
            "brief": brief
        }
    )


@login_required(login_url="partner_login")
@require_POST
def reuse_brief(request, brief_id):
    original = get_object_or_404(
        PlacementBrief,
        id=brief_id,
        owner=request.user
    )

    new_brief = PlacementBrief.objects.create(
        owner=request.user,
        status="draft",
        organisation_name=original.organisation_name,
        contact_name=original.contact_name,
        contact_email=original.contact_email,
        position_title=original.position_title,
        location=original.location,
        position_description=original.position_description,
        number_of_positions=original.number_of_positions,
    )

    new_brief.disciplines.set(
        original.disciplines.all()
    )

    new_brief.duties.set(
        original.duties.all()
    )

    messages.success(
        request,
        "A new draft was created from the previous Placement Brief."
    )

    return redirect(
        "edit_brief",
        brief_id=new_brief.id
    )


@login_required(login_url="partner_login")
def edit_brief(request, brief_id):
    brief = get_object_or_404(
        PlacementBrief,
        id=brief_id,
        owner=request.user,
        status="draft"
    )

    if request.method == "POST":
        form = EPlacementForm(
            request.POST,
            instance=brief
        )

        if form.is_valid():
            action = request.POST.get("action")

            if action == "submit":
                required_fields = [
                    "organisation_name",
                    "contact_name",
                    "contact_email",
                    "position_title",
                    "position_description",
                    "disciplines",
                    "duties",
                ]

                missing_fields = False

                for field in required_fields:
                    if not form.cleaned_data.get(field):
                        form.add_error(
                            field,
                            "This field is required before submitting."
                        )
                        missing_fields = True

                if missing_fields:
                    return render(
                        request,
                        "placements/brief_form.html",
                        {
                            "form": form,
                            "page_name": "Continue Placement Brief",
                        }
                    )

            brief = form.save(commit=False)

            if action == "submit":
                brief.status = "submitted"
                brief.submitted_at = timezone.now()

                message = (
                    "Placement Brief submitted and is "
                    "waiting for approval."
                )

            else:
                brief.status = "draft"
                message = "Draft updated successfully."

            brief.save()
            form.save_m2m()

            messages.success(
                request,
                message
            )

            return redirect("my_briefs")

    else:
        form = EPlacementForm(
            instance=brief
        )

    return render(
        request,
        "placements/brief_form.html",
        {
            "form": form,
            "page_name": "Continue Placement Brief",
        }
    )


@login_required(login_url="partner_login")
def ltt_dashboard(request):
    if not is_ltt(request.user):
        return HttpResponseForbidden(
            "You do not have permission to view this page."
        )

    all_briefs = PlacementBrief.objects.exclude(
        status="draft"
    )

    briefs = all_briefs.prefetch_related(
        "disciplines",
        "duties"
    )

    selected_status = request.GET.get(
        "status",
        ""
    )

    selected_discipline = request.GET.get(
        "discipline",
        ""
    )

    if selected_status in [
        "submitted",
        "approved"
    ]:
        briefs = briefs.filter(
            status=selected_status
        )

    if selected_discipline.isdigit():
        briefs = briefs.filter(
            disciplines__id=int(selected_discipline)
        )

    briefs = briefs.distinct().order_by(
        "-submitted_at"
    )

    disciplines = Discipline.objects.filter(
        active=True
    )

    context = {
        "briefs": briefs,
        "disciplines": disciplines,
        "selected_status": selected_status,
        "selected_discipline": selected_discipline,
        "total_count": all_briefs.count(),
        "waiting_count": all_briefs.filter(
            status="submitted"
        ).count(),
        "approved_count": all_briefs.filter(
            status="approved"
        ).count(),
    }

    return render(
        request,
        "placements/ltt_dashboard.html",
        context
    )


@login_required(login_url="partner_login")
def ltt_brief_detail(request, brief_id):
    if not is_ltt(request.user):
        return HttpResponseForbidden(
            "You do not have permission to view this page."
        )

    brief = get_object_or_404(
        PlacementBrief.objects.exclude(
            status="draft"
        ),
        id=brief_id
    )

    return render(
        request,
        "placements/ltt_brief_info.html",
        {
            "brief": brief
        }
    )


@login_required(login_url="partner_login")
def export_briefs(request):
    if not is_ltt(request.user):
        return HttpResponseForbidden(
            "You do not have permission to export this data."
        )

    briefs = PlacementBrief.objects.exclude(
        status="draft"
    ).prefetch_related(
        "disciplines",
        "duties"
    )

    selected_status = request.GET.get(
        "status",
        ""
    )

    selected_discipline = request.GET.get(
        "discipline",
        ""
    )

    if selected_status in [
        "submitted",
        "approved"
    ]:
        briefs = briefs.filter(
            status=selected_status
        )

    if selected_discipline.isdigit():
        briefs = briefs.filter(
            disciplines__id=int(selected_discipline)
        )

    briefs = briefs.distinct().order_by(
        "-submitted_at"
    )

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="placement_briefs.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Brief ID",
        "Organisation",
        "Position",
        "Disciplines",
        "Duties",
        "Submitted",
        "Status",
    ])

    for brief in briefs:
        disciplines = ", ".join(
            discipline.name
            for discipline in brief.disciplines.all()
        )

        duties = ", ".join(
            duty.name
            for duty in brief.duties.all()
        )

        submitted_date = ""

        if brief.submitted_at:
            submitted_date = brief.submitted_at.strftime(
                "%d %b %Y %H:%M"
            )

        writer.writerow([
            brief.id,
            brief.organisation_name,
            brief.position_title,
            disciplines,
            duties,
            submitted_date,
            brief.get_status_display(),
        ])

    return response


@login_required(login_url="partner_login")
def academic_reviews(request, brief_id=None):
    if not is_academic(request.user):
        return HttpResponseForbidden(
            "You do not have permission to review Placement Briefs."
        )

    briefs = PlacementBrief.objects.filter(
        status="submitted"
    ).prefetch_related(
        "disciplines",
        "duties"
    ).order_by(
        "-submitted_at"
    )

    selected_brief = None

    if brief_id is not None:
        selected_brief = get_object_or_404(
            PlacementBrief,
            id=brief_id,
            status="submitted"
        )

        if request.method == "POST":
            comments = request.POST.get(
                "comments",
                ""
            ).strip()

            Review.objects.create(
                brief=selected_brief,
                reviewer=request.user,
                outcome="approved",
                comments=comments
            )

            selected_brief.status = "approved"
            selected_brief.save()

            messages.success(
                request,
                "Placement Brief approved successfully."
            )

            return redirect(
                "academic_reviews"
            )

    return render(
        request,
        "placements/academic_reviews.html",
        {
            "briefs": briefs,
            "selected_brief": selected_brief,
        }
    )


def partner_signup(request):
    if request.method == "POST":
        form = PartnerSignupForm(
            request.POST
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created. Please sign in."
            )

            return redirect(
                "partner_login"
            )

    else:
        form = PartnerSignupForm()

    return render(
        request,
        "placements/signup.html",
        {
            "form": form
        }
    )


class PartnerLoginView(LoginView):
    authentication_form = PartnerLoginForm
    template_name = "placements/login.html"

    def get_success_url(self):
        if is_ltt(self.request.user):
            return reverse(
                "ltt_dashboard"
            )

        if is_academic(self.request.user):
            return reverse(
                "academic_reviews"
            )

        return reverse(
            "my_briefs"
        )