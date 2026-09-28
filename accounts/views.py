from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags

from accounts.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Profile
from .forms import ProfileForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = True
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = request.get_host()

            send_verification_email(user, domain, uid, token)

            # send activation email
            subject = 'Activate Your WarehouseIMS Account'
            html_content = render_to_string('accounts/activate_account.html', {
                'user': user,
                'uid': uid,
                'token': token,
                'domain': domain,
            })

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject,
                text_content,
                'WarehouseIMS <juvenpinoy@gmail.com>',
                [user.email],
            )

            email.attach_alternative(html_content, 'text/html')
            email.send()

            role_msg = user.role

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

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None in default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, "Account has been successfully activated! You are now able to log in.")
        else:
            messages.error(request, "Your account is already active. Please log in again.")
        return redirect('login')

    else:
        messages.error(request, "Activation link is invalid. Please check your email and try again.")
    return redirect('login')

def send_verification_email(user, domain, uid, token):
    subject = 'Activate your WarehouseIMS account'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    html_content = render_to_string('account/activate_account.html', {
        'user': user,
        'domain': domain,
        'uid': uid,
        'token': token,
    })

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content,  'text/html')

    email.send()


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