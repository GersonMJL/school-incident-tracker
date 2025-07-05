from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from users.models import SchoolAdmin


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        self.fields["username"].label = "Email"
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Email"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Senha"}
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Email"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Senha"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirme Senha"}
        )


class SchoolAdminCreationForm(forms.ModelForm):
    class Meta:
        model = SchoolAdmin
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Nome"}
        )


class SchoolAdminPageForm(forms.ModelForm):
    """Form to handle user-related fields including password change."""

    password = forms.CharField(
        widget=forms.PasswordInput, required=False, label="Password"
    )

    class Meta:
        model = SchoolAdmin
        fields = ("user", "name")

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            # If password is provided, it will be set during save
            self.instance.user.set_password(password)
        return password


class PasswordChangeForm(PasswordChangeForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirme Nova Senha"
    )

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get("new_password1")
        confirm_password = self.cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("As duas senhas devem ser iguais.")
        return confirm_password
