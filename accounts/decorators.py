from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth.decorators import user_passes_test


# -----------------------
# 1. GROUP BASED DECORATOR (optional)
# -----------------------

def group_required(group_name):
    def in_group(user):
        return user.is_authenticated and (
            user.groups.filter(name=group_name).exists() or user.is_superuser
        )
    return user_passes_test(in_group)


# -----------------------
# 2. ROLE BASED DECORATORS
# -----------------------

def role_required(*allowed_roles):
    """General role checker: multiple allowed roles"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user

            if not user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")

            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            if user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden("Access denied: insufficient role permissions.")
        return _wrapped
    return decorator


# ---- Specific decorators ----

def cadet_required(view_func):
    return role_required("CADET")(view_func)


def faculty_required(view_func):
    return role_required("FACULTY")(view_func)


def admin_required(view_func):
    return role_required("ADMIN")(view_func)


def higher_faculty_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return HttpResponseForbidden("You must be logged in.")

        if user.is_superuser:
            return view_func(request, *args, **kwargs)

        if user.role == "FACULTY" and user.is_higher_faculty:
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden("Access restricted: Higher Faculty only.")
    return _wrapped
