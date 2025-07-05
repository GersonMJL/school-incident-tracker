import io
from io import BytesIO

import boto3
import pytz
from django.conf import settings
from django.core.mail import EmailMessage
from incidents.models import IncidentReport
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


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

    brt_timezone = pytz.timezone("America/Sao_Paulo")
    localized_created_at = incident_report.created_at.astimezone(brt_timezone)

    # Prepare the content
    content = [
        Paragraph("Relatório de ocorrência", styles["Title"]),
        Spacer(1, 12),
        Paragraph(
            "Aluno:",
            bold_style,
        ),
        Paragraph(
            f"{incident_report.student.name} - {incident_report.student.school_id}",
            styles["Normal"],
        ),
        Spacer(1, 12),
        Paragraph(
            "Tipo de ocorrência:",
            bold_style,
        ),
        Paragraph(
            f"{incident_report.incident_type.name}",
            styles["Normal"],
        ),
        Spacer(1, 12),
        Paragraph("Descrição:", bold_style),
        Paragraph(f"{incident_report.description}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph(
            "Data de geração de relatório:",
            bold_style,
        ),
        Paragraph(f"{localized_created_at.strftime('%d/%m/%Y')}", styles["Normal"]),
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
    s3_buffer = BytesIO(pdf_buffer.getvalue())
    # Initialize S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    brt_timezone = pytz.timezone("America/Sao_Paulo")
    localized_created_at = incident_report.created_at.astimezone(brt_timezone)

    # Generate a s3 url for the file
    filename = f"{incident_report.student.name}_{localized_created_at.strftime('%d%m%Y_%H%M%S')}.pdf"
    pdf_url = (
        f"https://cepa-incidents.s3.sa-east-1.amazonaws.com/incident_reports/{filename}"
    )

    # Upload to S3
    s3_client.upload_fileobj(
        s3_buffer,
        settings.AWS_STORAGE_BUCKET_NAME,
        f"incident_reports/{filename}",
        ExtraArgs={"ContentType": "application/pdf"},
    )

    # Store the S3 file url in the model
    incident_report.pdf_file = pdf_url
    incident_report.save()


def send_incident_report_email(incident_report: IncidentReport, pdf_buffer: BytesIO):
    """
    Send email with incident report PDF attachment

    :param incident_report: IncidentReport instance
    :param pdf_buffer: BytesIO buffer containing PDF
    """
    # Determine recipient email
    # This is a placeholder - you'll need to modify based on your specific requirements
    email_buffer = BytesIO(pdf_buffer.getvalue()).getvalue()

    recipient_email = [incident_report.created_by.user.email]

    if incident_report.student.email:
        recipient_email.append(incident_report.student.email)
    if incident_report.student.parent_email:
        recipient_email.append(incident_report.student.parent_email)

    brt_timezone = pytz.timezone("America/Sao_Paulo")
    localized_created_at = incident_report.created_at.astimezone(brt_timezone)

    # Prepare email
    email = EmailMessage(
        subject=f"Incident Report for {incident_report.student.name}",
        body=f"""
        Prezados(as),

        Um relatório de incidente referente à {incident_report.student.name} com matrícula {incident_report.student.school_id} foi registrado com os seguintes detalhes:

        Tipo de incidente: {incident_report.incident_type.name}
        Data: {localized_created_at.strftime('%d/%m/%Y')}

        Segue em anexo o relatório detalhado.

        Atenciosamente,
        Administração da Escola Moreira e Silva
        """,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Set in your Django settings
        to=recipient_email,
    )

    # Attach PDF
    # Generate filename for attachment
    filename = f"Relatorio_de_Incidente_{incident_report.student.name}_{incident_report.created_at.strftime('%d%m%Y_%H%M%S')}.pdf"

    # Attach the PDF
    email.attach(filename, email_buffer, "application/pdf")

    # Send email
    email.send()
