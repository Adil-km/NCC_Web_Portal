from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import (
    User,
    UserTag,
    UserTagAssignment,
)

# ------------------------------------------------------------------
# Custom User Admin (UNCHANGED as requested)
# ------------------------------------------------------------------

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
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields shown when creating a user
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

# ------------------------------------------------------------------
# UserTag Admin (Create / Delete permission tags)
# ------------------------------------------------------------------

@admin.register(UserTag)
class UserTagAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at")
    search_fields = ("name", "code")
    ordering = ("name",)


# ------------------------------------------------------------------
# UserTagAssignment Admin (Assign tags to users)
# ------------------------------------------------------------------

@admin.register(UserTagAssignment)
class UserTagAssignmentAdmin(admin.ModelAdmin):
    list_display = ("user", "tag", "assigned_at")
    list_filter = ("tag",)
    search_fields = ("user__username", "tag__code")
    autocomplete_fields = ("user", "tag")
