from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Student, IncidentType
from .forms import StudentForm, IncidentTypeForm, IncidentReportForm


@login_required
def list_students(request):
    students = Student.objects.all()
    return render(request, "incidents/student_list.html", {"students": students})


@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_students")
    else:
        form = StudentForm()
    return render(request, "incidents/student_form.html", {"form": form})


@login_required
def list_incident_types(request):
    incident_types = IncidentType.objects.all()
    return render(
        request, "incidents/incident_type_list.html", {"incident_types": incident_types}
    )


@login_required
def add_incident_type(request):
    if request.method == "POST":
        form = IncidentTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_incident_types")
    else:
        form = IncidentTypeForm()
    return render(request, "incidents/incident_type_form.html", {"form": form})


@login_required
def create_incident_report(request):
    form = IncidentReportForm()

    if request.method == "POST":
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_students")
    else:
        form = IncidentReportForm()
    return render(request, "incidents/incident_report_form.html", {"form": form})
