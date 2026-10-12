from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EPlacementForm


def create_brief(request):
    if request.method == "POST":
        form = EPlacementForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Placement brief submitted successfully.")
            return redirect("create_brief")
    else:
        form = EPlacementForm()

    return render(request, "placements/brief_form.html", {"form": form})