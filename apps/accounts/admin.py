from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm

# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [
        "username",
        "email",
        "phone_number",
        "is_admin",
        "is_verified",
        "national_code",
    ]
    list_filter = ["username", "email", "phone_number", "is_admin"]
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("phone_number", "national_code")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "username",
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                    "national_code",
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                ],
            },
        ),
    ]
    search_fields = ("email", "username", "phone_number")
    ordering = ("username",)
    filter_horizontal = []


admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_birth")
    search_fields = ("first_name", "last_name")


admin.site.register(Profile, ProfileAdmin)
