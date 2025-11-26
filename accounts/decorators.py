from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth.decorators import user_passes_test

def group_required(group_name):
    def in_group(user):
        return user.groups.filter(name=group_name).exists() or user.is_superuser
    return user_passes_test(in_group)

def cadet_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'CADET' or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page (Cadet Only).")
    return _wrapped_view

def faculty_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'FACULTY' or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page (Faculty Only).")
    return _wrapped_view

def higher_faculty_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'FACULTY' and request.user.is_higher_faculty:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Restricted: Higher Faculty Access Only.")
    return _wrapped_view