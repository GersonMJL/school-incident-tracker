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


class IncidentFilterForm(forms.Form):
    incident_type = forms.ModelChoiceField(
        queryset=IncidentType.objects.all(),
        required=False,
        empty_label="Todos os tipos",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    date_from = forms.DateField(
        required=False,
        label="De",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    date_to = forms.DateField(
        required=False,
        label="Até",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Pesquise por matrícula..."}
        ),
    )
