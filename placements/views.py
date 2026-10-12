from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import EPlacementForm, PartnerSignupForm, PartnerLoginForm
from .models import PlacementBrief


# Creates a new Placement Brief
@login_required(login_url="partner_login")
def create_brief(request):
    if request.method == "POST":
        form = EPlacementForm(request.POST)

        if form.is_valid():
            action = request.POST.get("action")

            # These fields must be completed before final submission
            if action == "submit":
                required_fields = [
                    "organisation_name",
                    "contact_name",
                    "contact_email",
                    "position_title",
                    "position_description",
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
                message = "Placement Brief submitted successfully."
            else:
                brief.status = "draft"
                message = "Draft saved successfully."

            brief.save()

            messages.success(request, message)
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


# Shows the logged-in partner's Placement Briefs
@login_required(login_url="partner_login")
def my_briefs(request):
    briefs = PlacementBrief.objects.filter(
        owner=request.user
    ).order_by("-updated_at")

    return render(
        request,
        "placements/my_briefs.html",
        {"briefs": briefs}
    )


# Shows one Placement Brief as a read-only page
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
        {"brief": brief}
    )


# Creates a new draft using an existing Placement Brief
@login_required(login_url="partner_login")
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

    messages.success(
        request,
        "A new draft was created from the previous Placement Brief."
    )

    return redirect(
        "edit_brief",
        brief_id=new_brief.id
    )


# Allows the partner to reopen and continue one of their drafts
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

            # Final submission requires the main fields
            if action == "submit":
                required_fields = [
                    "organisation_name",
                    "contact_name",
                    "contact_email",
                    "position_title",
                    "position_description",
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
                message = "Placement Brief submitted successfully."
            else:
                brief.status = "draft"
                message = "Draft updated successfully."

            brief.save()

            messages.success(request, message)
            return redirect("my_briefs")

    else:
        form = EPlacementForm(instance=brief)

    return render(
        request,
        "placements/brief_form.html",
        {
            "form": form,
            "page_name": "Continue Placement Brief",
        }
    )


# Creates a partner account and sends them to the login page
def partner_signup(request):
    if request.method == "POST":
        form = PartnerSignupForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created. Please sign in."
            )

            return redirect("partner_login")

    else:
        form = PartnerSignupForm()

    return render(
        request,
        "placements/signup.html",
        {"form": form}
    )


# Uses Django's login system to sign in a partner
class PartnerLoginView(LoginView):
    authentication_form = PartnerLoginForm
    template_name = "placements/login.html"