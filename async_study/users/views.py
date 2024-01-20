from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("flashcards")
    if request.method == "POST":
        username = request.POST.get("username") or ""
        password = request.POST.get("password") or ""
        confirm_password = request.POST.get("confirm_password") or ""
        if username.strip() == "" or password.strip() == "":
            messages.error(request, "Please fill in all fields")
            return redirect("sign_up")
        if len(password.strip()) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect("sign_up")
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("sign_up")
        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return redirect("sign_up")
        if " " in password:
            messages.error(request, "Password cannot contain spaces")
            return redirect("sign_up")
        try:
            user = User.objects.create_user(username, password=password)
            messages.success(request, "User created successfully")
            login(request, user)
            return redirect("flashcards")
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect("sign_up")
    return render(request, "sign_up.html")


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("flashcards")
    if request.method == "POST":
        username = request.POST.get("username") or ""
        password = request.POST.get("password") or ""
        if username.strip() == "" or password.strip() == "":
            messages.error(request, "Please fill in all fields")
            return redirect("sign_in")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("flashcards")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("sign_in")
    return render(request, "sign_in.html")


def sign_out(request):
    logout(request)
    return redirect("sign_in")
