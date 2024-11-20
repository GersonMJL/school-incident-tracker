from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.http import HttpResponse

User = get_user_model()


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        # Create user but do not activate
        user = User.objects.create_user(
            username=username, email=email, password=password, is_active=False
        )

        # Generate a confirmation code
        confirmation_code = get_random_string(length=32)
        user.confirmation_code = confirmation_code
        user.save()

        # Send the email
        confirmation_url = request.build_absolute_uri(
            reverse("confirm_email", args=[confirmation_code])
        )
        send_mail(
            "Confirm Your Email",
            f"Click the link to confirm your email: {confirmation_url}",
            "noreply@example.com",
            [email],
        )
        return redirect("registration_complete")
    return render(request, "register.html")


def confirm_email(request, confirmation_code):
    user = get_object_or_404(User, confirmation_code=confirmation_code)
    user.is_active = True
    user.is_email_verified = True
    user.confirmation_code = None  # Clear the code
    user.save()
    return HttpResponse("Your email has been confirmed. You can now log in.")
