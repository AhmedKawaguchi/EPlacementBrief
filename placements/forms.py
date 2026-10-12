from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import PlacementBrief


# Creates the placement brief form
class EPlacementForm(forms.ModelForm):
    class Meta:
        model = PlacementBrief
        fields = [
            "organisation_name",
            "contact_name",
            "contact_email",
            "position_title",
            "location",
            "position_description",
            "number_of_positions",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        optional_for_draft = [
            "organisation_name",
            "contact_name",
            "contact_email",
            "position_title",
            "location",
            "position_description",
        ]

        for field in optional_for_draft:
            self.fields[field].required = False

    def clean_number_of_positions(self):
        number = self.cleaned_data["number_of_positions"]

        if number < 1:
            raise forms.ValidationError("Enter at least 1 position.")

        return number


# Creates a partner account using an email and password
class PartnerSignupForm(UserCreationForm):
    username = forms.EmailField(label="Email", max_length=150)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def clean_username(self):
        email = self.cleaned_data["username"].strip().lower()

        if User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["username"]

        if commit:
            user.save()

        return user


# Signs in a partner using their email and password
class PartnerLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=150)

    def clean_username(self):
        return self.cleaned_data["username"].strip().lower()