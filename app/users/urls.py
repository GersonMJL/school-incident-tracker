from django.urls import path
from . import views

urlpatterns = [
    # path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    # path(
    #     "registration-complete/",
    #     views.registration_complete,
    #     name="registration_complete",
    # ),
    # path("confirm/<str:confirmation_code>/", views.confirm_email, name="confirm_email"),
]
