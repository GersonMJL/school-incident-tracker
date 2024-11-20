import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import boto3
from django.conf import settings
from incidents.models import IncidentReport


def generate_incident_report_pdf(incident_report: IncidentReport):
    """
    Generate a PDF for the incident report

    :param incident_report: IncidentReport instance
    :return: BytesIO buffer containing the PDF
    """
    # Create a buffer for the PDF
    buffer = io.BytesIO()

    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    bold_style = ParagraphStyle(
        "BoldStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor="black",
    )

    # Prepare the content
    content = [
        Paragraph(f"Relatório de ocorrência", styles["Title"]),
        Spacer(1, 12),
        Paragraph(
            f"Aluno:",
            bold_style,
        ),
        Paragraph(
            f"{incident_report.student.name} - {incident_report.student.school_id}",
            styles["Normal"],
        ),
        Spacer(1, 12),
        Paragraph(
            f"Tipo de ocorrência:",
            bold_style,
        ),
        Paragraph(
            f"{incident_report.incident_type.name}",
            styles["Normal"],
        ),
        Spacer(1, 12),
        Paragraph(f"Descrição:", bold_style),
        Paragraph(f"{incident_report.description}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph(
            f"Data de geração de relatório:",
            bold_style,
        ),
        Paragraph(
            f"{incident_report.created_at.strftime('%d/%m/%Y')}", styles["Normal"]
        ),
    ]

    # Build PDF
    doc.build(content)

    # Move buffer position to the beginning
    buffer.seek(0)

    return buffer


def upload_pdf_to_s3(pdf_buffer, incident_report):
    """
    Upload PDF to S3 bucket

    :param pdf_buffer: BytesIO buffer containing PDF
    :param incident_report: IncidentReport instance
    """
    # Initialize S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    # Generate a unique filename
    filename = f"incident_reports/{incident_report.student.name}_{incident_report.created_at.strftime('%d-%m-%Y_%H-%M-%S')}.pdf"

    # Upload to S3
    s3_client.upload_fileobj(
        pdf_buffer,
        settings.AWS_STORAGE_BUCKET_NAME,
        filename,
        ExtraArgs={"ContentType": "application/pdf"},
    )

    # Store the S3 file path in the model
    incident_report.pdf_file = filename
    incident_report.save()
