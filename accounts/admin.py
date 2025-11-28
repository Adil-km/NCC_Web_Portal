from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    # Fields shown when editing a user
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Role Information", {
            "fields": ("role", "is_higher_faculty", "assigned_faculty")
        }),
        ("Permissions", {
            "fields": (
                "is_active", "is_staff", "is_superuser",
                "groups", "user_permissions"
            )
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields shown when CREATING a user (important)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "password1",
                "password2",
                "role",
                "is_higher_faculty",
                "assigned_faculty",
                "is_staff",
                "is_superuser",
                "groups",
            ),
        }),
    )

    list_display = ["username", "email", "role", "is_higher_faculty", "is_staff"]
    list_filter = ["role", "is_higher_faculty", "is_staff", "is_superuser"]


admin.site.register(User, CustomUserAdmin)
