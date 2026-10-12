from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import PlacementBrief, Discipline, Duty


class DutySelectMultiple(forms.SelectMultiple):
    def create_option(
        self,
        name,
        value,
        label,
        selected,
        index,
        subindex=None,
        attrs=None
    ):
        option = super().create_option(
            name,
            value,
            label,
            selected,
            index,
            subindex,
            attrs
        )

        if value and hasattr(value, "instance"):
            duty = value.instance

            option["attrs"]["data-discipline"] = str(
                duty.discipline_id
            )

        return option


class EPlacementForm(forms.ModelForm):
    disciplines = forms.ModelMultipleChoiceField(
        queryset=Discipline.objects.filter(active=True),
        required=False,
        widget=forms.SelectMultiple
    )

    duties = forms.ModelMultipleChoiceField(
        queryset=Duty.objects.filter(active=True),
        required=False,
        widget=DutySelectMultiple
    )

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
            "disciplines",
            "duties",
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
            "disciplines",
            "duties",
        ]

        for field in optional_for_draft:
            self.fields[field].required = False

    def clean_number_of_positions(self):
        number = self.cleaned_data["number_of_positions"]

        if number < 1:
            raise forms.ValidationError(
                "Enter at least 1 position."
            )

        return number

    def clean(self):
        cleaned_data = super().clean()

        disciplines = cleaned_data.get("disciplines")
        duties = cleaned_data.get("duties")

        if disciplines and duties:
            selected_discipline_ids = set(
                disciplines.values_list(
                    "id",
                    flat=True
                )
            )

            for duty in duties:
                if duty.discipline_id not in selected_discipline_ids:
                    self.add_error(
                        "duties",
                        (
                            f"{duty.name} does not belong "
                            "to a selected discipline."
                        )
                    )

        return cleaned_data


class PartnerSignupForm(UserCreationForm):
    username = forms.EmailField(
        label="Email",
        max_length=150
    )

    class Meta:
        model = User

        fields = [
            "username",
            "password1",
            "password2",
        ]

    def clean_username(self):
        email = (
            self.cleaned_data["username"]
            .strip()
            .lower()
        )

        if User.objects.filter(
            username__iexact=email
        ).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data[
            "username"
        ]

        if commit:
            user.save()

        return user


class PartnerLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        max_length=150
    )

    def clean_username(self):
        return (
            self.cleaned_data["username"]
            .strip()
            .lower()
        )