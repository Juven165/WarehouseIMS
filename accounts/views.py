from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

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
        messages.success(request, f"Welcome back{user.username}!")
        return redirect('admin_dashboard')


    elif user.role == 'staff':
        messages.success(request, f"Welcome back{user.username}!")
        return redirect('staff_dashboard')

    elif user.role == 'supplier':
        messages.success(request, f"Welcome back{user.username}!")
        return redirect('supplier_dashboard')

    else:
        messages.error(request, f"Invalid username or account not found please register first.")
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
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")

def logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect('login')