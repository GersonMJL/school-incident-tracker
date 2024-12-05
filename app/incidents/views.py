from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Student, IncidentType, IncidentReport
from .forms import StudentForm, IncidentTypeForm, IncidentReportForm
from django.core.paginator import Paginator
from django.contrib import messages
from .utils import (
    generate_incident_report_pdf,
    upload_pdf_to_s3,
    send_incident_report_email,
)
from django.db.models import Q
from .models import IncidentReport
from .forms import IncidentFilterForm


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
            form.instance.created_by = request.user.school_admin_profile
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


@login_required
def incident_list(request):
    # Initialize the filter form
    filter_form = IncidentFilterForm(request.GET)

    # Start with all incidents
    queryset = IncidentReport.objects.select_related(
        "student", "incident_type", "created_by"
    ).order_by("-created_at")

    # Apply filters if form is valid
    if filter_form.is_valid():
        # Filter by incident type
        if filter_form.cleaned_data["incident_type"]:
            queryset = queryset.filter(
                incident_type=filter_form.cleaned_data["incident_type"]
            )

        # Filter by date range
        # if filter_form.cleaned_data["date_from"]:
        #     queryset = queryset.filter(
        #         created_at__date__gte=filter_form.cleaned_data["date_from"]
        #     )
        # if filter_form.cleaned_data["date_to"]:
        #     queryset = queryset.filter(
        #         created_at__date__lte=filter_form.cleaned_data["date_to"]
        #     )

        # Search by student name
        if filter_form.cleaned_data["search"]:
            search_query = filter_form.cleaned_data["search"]
            queryset = queryset.filter(
                Q(student__name__icontains=search_query)
                | Q(student__school_id__icontains=search_query)
            )

    # Pagination
    paginator = Paginator(queryset, 10)  # Show 10 incidents per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "incidents": page_obj,
        "filter_form": filter_form,
        "title": "Incident Reports",
    }
    return render(request, "incidents/incident_list.html", context)


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Estudante atualizado com sucesso.")
    else:
        form = StudentForm(instance=student)
    return redirect("list_students")
