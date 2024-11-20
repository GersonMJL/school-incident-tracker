from django import forms
from .models import Student, IncidentType, IncidentReport
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "email", "parent_email", "school_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit", css_class="btn btn-primary"))


class IncidentTypeForm(forms.ModelForm):
    class Meta:
        model = IncidentType
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit", css_class="btn btn-primary"))


class IncidentReportForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-select searchable-select", "data-search": "true"}
        ),
    )

    class Meta:
        model = IncidentReport
        fields = ["student", "incident_type", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit", css_class="btn btn-primary"))
