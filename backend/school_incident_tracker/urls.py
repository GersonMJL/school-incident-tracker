from django.contrib import admin
from django.urls import include, path
from incidents.views import create_incident_report

urlpatterns = [
    path("", create_incident_report, name="create_incident_report"),
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls")),
    path("incidents/", include("incidents.urls")),
]
