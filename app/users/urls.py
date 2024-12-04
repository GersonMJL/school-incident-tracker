from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "reset-password/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset/password_reset.html",
            email_template_name="password_reset/password_reset_email.html",
            subject_template_name="password_reset/password_reset_subject.txt",
            success_url="sent/",
        ),
        name="password_reset",
    ),
    path(
        "reset-password/sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
