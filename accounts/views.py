from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Profile
from .forms import ProfileForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = True
            user.save()
            messages.success(request, 'Account created for ' + user.username)
            return redirect('login')

    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def dashboard(request):
    user = request.user

    print(user.role)

    if user.role == 'admin':
        messages.success(request, f"Welcome back, {user.username}!")
        return redirect('admin_dashboard')

    elif user.role == 'staff':
        messages.success(request, f"Welcome back, {user.username}!")
        return redirect('staff_dashboard')

    elif user.role == 'supplier':
        messages.success(request, f"Welcome back, {user.username}!")
        return redirect('supplier_dashboard')

    else:
        messages.error(
            request,
            "Invalid username or account not found. Please register first."
        )
        return redirect('login')

def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Clear old messages before successful login
            storage = messages.get_messages(request)
            list(storage)

            login(request, user)
            return redirect("dashboard")

        else:
            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "accounts/login.html")

def logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect('login')

@login_required
def my_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('my_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/my_profile.html', {
        'form': form,
        'profile': profile
    })