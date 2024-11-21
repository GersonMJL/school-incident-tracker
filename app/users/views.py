from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, authenticate, login
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )


# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Add Bootstrap classes to all form fields
#         for fieldname in self.fields:
#             self.fields[fieldname].widget.attrs.update({"class": "form-control"})


# def register_view(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.email = form.cleaned_data["email"]

#             confirmation_code = get_random_string(length=32)
#             user.confirmation_code = confirmation_code
#             user.save()

#             # Build the confirmation URL
#             confirmation_url = request.build_absolute_uri(
#                 reverse("confirm_email", args=[confirmation_code])
#             )

#             # Render email template
#             email_html = render_to_string(
#                 "accounts/emails/confirmation_email.html",
#                 {
#                     "confirmation_url": confirmation_url,
#                 },
#             )

#             # Send email
#             send_mail(
#                 subject="Confirm Your Email",
#                 message=f"Click the link to confirm your email: {confirmation_url}",
#                 html_message=email_html,
#                 from_email="noreply@example.com",
#                 recipient_list=[user.email],
#                 fail_silently=False,
#             )

#             messages.success(
#                 request,
#                 "Registration successful. Please check your email to confirm your account.",
#             )
#             return redirect("registration_complete")
#     else:
#         form = CustomUserCreationForm()

#     return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Welcome back, {username}!")
                    return redirect("create_incident_report")
                else:
                    messages.error(
                        request, "Please confirm your email before logging in."
                    )
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm(request)

    return render(request, "accounts/login.html", {"form": form})


# def confirm_email(request, confirmation_code):
#     try:
#         user = User.objects.get(confirmation_code=confirmation_code)
#         user.is_active = True
#         user.is_email_verified = True
#         user.confirmation_code = None
#         user.save()

#         messages.success(request, "Your email has been confirmed. You can now log in.")
#         return redirect("login")
#     except User.DoesNotExist:
#         messages.error(request, "Invalid confirmation link.")
#         return redirect("login")


# def registration_complete(request):
#     return render(request, "accounts/registration_complete.html")
