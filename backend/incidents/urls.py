from django.urls import path

from . import views

urlpatterns = [
    path("students/", views.list_students, name="list_students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/edit/<int:id>/", views.edit_student, name="edit_student"),
    path("incident-types/", views.list_incident_types, name="list_incident_types"),
    path("incident-types/add/", views.add_incident_type, name="add_incident_type"),
    path("", views.incident_list, name="incident_list"),
]
