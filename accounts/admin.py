from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    UserTag,
    UserTagAssignment,
)

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Role Information", {
            "fields": ["role"]
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "user_permissions",
            )
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "password1",
                "password2",
                "role",
            ),
        }),
    )

    list_display = ["username", "email", "role"]
    list_filter = ["role", "is_superuser"]


admin.site.register(User, CustomUserAdmin)

@admin.register(UserTag)
class UserTagAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at")
    search_fields = ("name", "code")
    ordering = ("name",)

@admin.register(UserTagAssignment)
class UserTagAssignmentAdmin(admin.ModelAdmin):
    list_display = ("user", "tag", "assigned_at")
    list_filter = ("tag",)
    search_fields = ("user__username", "tag__code")
    autocomplete_fields = ("user", "tag")