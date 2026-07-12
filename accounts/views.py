from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from django.conf import settings

from .forms import LoginForm
from .models import User


# ==========================================================
# Login
# ==========================================================

def login_view(request):

    form = LoginForm(request.POST or None)

    error = None

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"].strip()

            password = form.cleaned_data["password"]

            remember = form.cleaned_data["remember_me"]

            # Login using mobile number

            if username.isdigit():

                try:

                    user = User.objects.get(
                        mobile_number=username
                    )

                    username = user.username

                except User.DoesNotExist:
                    pass

            user = authenticate(

                request,

                username=username,

                password=password

            )

            if user:

                login(request, user)

                if not remember:
                    request.session.set_expiry(0)

                return redirect("/")

            error = "Invalid Username/Mobile Number or Password."

    return render(

        request,

        "accounts/login.html",

        {

            "form": form,

            "error": error

        }

    )


# ==========================================================
# Logout
# ==========================================================

def logout_view(request):

    logout(request)

    return redirect("login")


# ==========================================================
# Forgot Username
# ==========================================================

def forgot_username(request):

    if request.method == "POST":

        email = request.POST.get("email").strip().lower()

        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:

            return render(

                request,

                "accounts/forgot_username.html",

                {

                    "error": "No account found with this email."

                }

            )

        send_mail(

            subject="Your Shiva Teja Infra CRM Username",

            message=(
                f"Hello {user.first_name},\n\n"
                f"Your username is:\n\n"
                f"{user.username}\n\n"
                f"If you did not request this email, you can ignore it."
            ),

            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[user.email],

            fail_silently=False,

        )

        return render(

            request,

            "accounts/username_sent.html",

            {

                "email": user.email

            }

        )

    return render(

        request,

        "accounts/forgot_username.html"

    )


# ==========================================================
# Change Password
# ==========================================================

@login_required

def change_password(request):

    form = PasswordChangeForm(

        request.user,

        request.POST or None

    )

    if request.method == "POST":

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(

                request,

                user

            )

            messages.success(

                request,

                "Password changed successfully."

            )

            return redirect("/")

    return render(

        request,

        "accounts/change_password.html",

        {

            "form": form

        }

    )