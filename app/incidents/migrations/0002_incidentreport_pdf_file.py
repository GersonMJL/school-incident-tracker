# Generated by Django 5.1.3 on 2024-11-20 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentreport',
            name='pdf_file',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
