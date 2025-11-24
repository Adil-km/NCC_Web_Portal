from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from accounts.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group


@permission_required('auth.adminr')
def assign_role(request, user_id, role_id):
    user = get_object_or_404(User, id=user_id)
    role = get_object_or_404(Group, id=role_id)

    user.groups.add(role)
    return redirect('user_detail', user_id=user.id)

@permission_required('auth.change_user')
def revoke_role(request, user_id, role_id):
    user = get_object_or_404(User, id=user_id)
    role = get_object_or_404(Group, id=role_id)

    user.groups.remove(role)
    return redirect('user_detail', user_id=user.id)




def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "All fields are required.")
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, "register.html")

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Registration successful.")
            return redirect("login")
        except IntegrityError:
            messages.error(request, "Username or email already taken.")

    return render(request, "register.html")


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')
