# Generated by Django 5.1.3 on 2024-11-30 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncidentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('parent_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('school_id', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncidentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('pdf_file', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.schooladmin')),
                ('incident_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='incidents.incidenttype')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidents.student')),
            ],
        ),
    ]
