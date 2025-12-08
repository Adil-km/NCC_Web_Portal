from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import AssignGroupForm, CreateGroupWithPermissionsForm
from accounts.decorators import (
    admin_required, 
    cadet_required, 
    faculty_required,
    higher_faculty_required,
    group_required,
    role_required
)

# Create your views here.

def dashboard(request):
    return render(request, 'dashboard/home.html')

@faculty_required
def faculty(request):
    return render(request, 'dashboard/faculty.html')

@cadet_required
def cadet(request):
    return render(request, 'dashboard/cadet.html')

@higher_faculty_required
def assign_group(request):
    if request.method == "POST":
        form = AssignGroupForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            group = form.cleaned_data["group"]
            user.groups.add(group)
            return redirect("assign-group")
    else:
        form = AssignGroupForm()

    return render(request, "dashboard/faculty.html", {"form": form})


@higher_faculty_required
def create_group(request):
    if request.method == "POST":
        form = CreateGroupWithPermissionsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            perms = form.cleaned_data["permissions"]

            group = Group.objects.create(name=name)
            group.permissions.set(perms)
            group.save()

            return redirect("create-group")
    else:
        form = CreateGroupWithPermissionsForm()

    return render(request, "dashboard/create_group.html", {"form": form})

