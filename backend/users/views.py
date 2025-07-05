from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    update_session_auth_hash,
)
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.shortcuts import redirect, render
from users.forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    PasswordChangeForm,
    SchoolAdminCreationForm,
)
from users.models import SchoolAdmin

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get(
                "username"
            )  # This is actually the email in your case
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    school_admin = SchoolAdmin.objects.get(user=user)
                    login(request, user)
                    messages.success(
                        request, f"Bem vindo(a) de volta, {school_admin.name}!"
                    )
                    return redirect("create_incident_report")
                else:
                    messages.error(
                        request,
                        "Sua conta não foi ativada ainda, por favor contate o administrador para ativar.",
                    )
            else:
                messages.error(request, "Email e/ou senha inválidos.")
    else:
        form = CustomAuthenticationForm(request)

    return render(request, "accounts/login.html", {"form": form})


@transaction.atomic
def register_view(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        school_admin_form = SchoolAdminCreationForm(request.POST)

        if user_form.is_valid() and school_admin_form.is_valid():
            # Generate a unique username
            username = user_form.cleaned_data["email"]
            # Add a unique identifier if needed
            if User.objects.filter(username=username).exists():
                username = f"{username}_{User.objects.count() + 1}"

            user = user_form.save(commit=False)
            user.username = username
            user.is_active = False
            user.save()

            # Associate the school_admin_form with the newly created user
            school_admin_profile = school_admin_form.save(commit=False)
            school_admin_profile.user = user
            school_admin_profile.save()

            messages.success(
                request,
                "Conta criada com sucesso, para ativar contate o administrador.",
            )
            return redirect("login")
    else:
        user_form = CustomUserCreationForm()
        school_admin_form = SchoolAdminCreationForm()

    return render(
        request,
        "accounts/register.html",
        {"user_form": user_form, "school_admin_form": school_admin_form},
    )


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Update the session to keep the user logged in after changing the password
            update_session_auth_hash(request, form.user)
            messages.success(request, "Sua senha foi alterada com sucesso!")
            return redirect("incident_list")
        else:
            messages.error(request, "Algum erro ocorreu, por favor tente novamente.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "accounts/change_password.html", {"form": form})
