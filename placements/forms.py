from django import forms
from .models import PlacementBrief

# Creates a form, checks the format of each field
class EPlacementForm(forms.ModelForm):
    class Meta:
        model = PlacementBrief
        fields = [
            "organisation_name",
            "contact_name",
            "contact_email",
            "position_title",
            "position_description",
            "number_of_positions",
        ]

    # Ensures at least 1 position is available before submitting
    def clean_number_of_positions(self):
        number = self.cleaned_data["number_of_positions"]
        if number < 1:
            raise forms.ValidationError("Enter at least 1 position.")
        return number