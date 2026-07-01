from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.core.exceptions import ValidationError
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password


class UserCreationForm(forms.ModelForm):
    """Form for creating regular users and superusers."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "username", "national_code"]

    def clean_password2(self):
        """Check both passwords match"""
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

    def save(self, commit=True):
        """Save hashed password"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Form used in admin for updating users."""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_verified",
            "national_code",
        ]


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "id": "password-field",
            }
        )
    )


class AuthenticationForm(DjangoAuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        if not user.is_verified:
            raise ValidationError("User is not verified.")


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "id": "password-field",
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "confirm password",
                "class": "form-control",
                "id": "-password-field",
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if not password or not confirm_password:
            return cleaned_data

        if password != confirm_password:
            self.add_error("confirm_password", "رمز عبور و تکرار آن یکسان نیستند.")
            return cleaned_data
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            self.add_error("password", e)

        return cleaned_data
