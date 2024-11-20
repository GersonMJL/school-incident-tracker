from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Student, IncidentType
from .forms import StudentForm, IncidentTypeForm, IncidentReportForm
from django.contrib import messages
from .utils import (
    generate_incident_report_pdf,
    upload_pdf_to_s3,
    send_incident_report_email,
)


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
    if request.method == "POST":
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            # Save the incident report
            form.instance.created_by = request.user
            incident_report = form.save()

            try:
                # Generate PDF
                pdf_buffer = generate_incident_report_pdf(incident_report)

                # Upload to S3
                upload_pdf_to_s3(pdf_buffer, incident_report)

                # Send email with PDF attachment
                send_incident_report_email(incident_report, pdf_buffer)

                messages.success(
                    request, "Incident report created and PDF stored successfully."
                )
                return redirect("list_students")

            except Exception as e:
                messages.error(request, f"Error creating PDF: {str(e)}")
                # Optionally, you might want to delete the incident report if PDF generation fails
                incident_report.delete()

    else:
        form = IncidentReportForm()

    return render(request, "incidents/incident_report_form.html", {"form": form})
