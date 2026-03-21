from django import forms
from apps.companies.models import Complaint


class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ["reason"]

        widgets = {
            "reason": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Reason...",
                "rows": 4
            })
        }

        labels = {
            "reason": "Reason"
        }

        help_texts = {
            "reason": "Specify what exactly violates this job posting."
        }
