from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import AssignRoleForm, CreateGroupWithPermissionsForm

# Create your views here.

def dashboard(request):
    return render(request, 'dashboard/home.html')

def faculty(request):
    return render(request, 'dashboard/faculty.html')

def cadet(request):
    return render(request, 'dashboard/cadet.html')


def assign_role_view(request):
    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            group = form.cleaned_data['group']
            
            # remove old roles if needed
            user.groups.clear()
            
            # assign new role
            user.groups.add(group)
            
            return redirect("assign-role")   # redirect to same page
    else:
        form = AssignRoleForm()

    return render(request, "dashboard/faculty.html", {"form": form})

def create_group_view(request):
    if request.method == "POST":
        form = CreateGroupWithPermissionsForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['name']
            permissions = form.cleaned_data['permissions']

            # Create new group
            group, created = Group.objects.get_or_create(name=group_name)

            # Add permissions
            group.permissions.set(permissions)

            return redirect("create-group")  # refresh page
    else:
        form = CreateGroupWithPermissionsForm()

    return render(request, "dashboard/create_group.html", {"form": form})