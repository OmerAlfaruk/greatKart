from email.message import EmailMessage
from django.shortcuts import redirect, render

from accounts.forms import RegistrationForm
from accounts.models import Account
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMessage


# Create your views here.


def register(request):
    """
    View to handle user registration.
    """

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            phone_number = form.cleaned_data.get("phone_number")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number

            user.save()
            # activate user
            current_site = get_current_site(request)
            # Here you would typically send an activation email
            mail_subject = "Please activate your account"
            message = render_to_string(
                "accounts/activation_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(
                        user
                    ),  # Assuming you have a method to generate this
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # You would send the email here using Django's email functionality

            return redirect("/accounts/login/?command=verification&email=" + email)

    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)


def login(request):
    """
    View to handle user login.
    """
    command = request.GET.get("command")
    email = request.GET.get("email")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("dashboard")  # Redirect to a suitable page after login
        else:
            messages.error(request, "Invalid email or password.")

    return render(
        request,
        "accounts/login.html",
        {
            "command": command,
            "email": email,
        },
    )


@login_required(login_url="login")
def logout(request):
    """View to handle user logout."""
    auth.logout(request)
    messages.success(request, "you are logged out")

    return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print("Decoded UID:", uid)
        user = Account._default_manager.get(pk=uid)
        print("User found:", user)
    except Exception as e:
        print("Error decoding UID or finding user:", e)
        user = None

    if user is not None:
        print("User is_active:", user.is_active)
        print("Token valid:", default_token_generator.check_token(user, token))

    if (
        user is not None
        and not user.is_active
        and default_token_generator.check_token(user, token)
    ):
        user.is_active = True
        user.save()
        messages.success(
            request, "Congratulations, your account has been activated successfully."
        )
        return redirect("login")
    else:
        messages.error(request, "Invalid or expired activation link.")
        return redirect("register")


@login_required(login_url="login")
def dashboard(request):
    """Render the user dashboard."""
    return render(request, "accounts/dashboard.html")


def forgot_passord(request):
    if request.method == "POST":
        email = request.POST["email"]

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            # Here you would typically send an activation email
            mail_subject = "reset your password"
            message = render_to_string(
                "accounts/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(
                        user
                    ),  # Assuming you have a method to generate this
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, "password reset email hasbeen sent to your email")
            return redirect("login")
        else:
            messages.error(request, "Account does not exist")
            return redirect("forgotpassword")

    return render(request, "accounts/forgotPassword.html")


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except Exception as e:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password")
        return redirect("resetpassword")
    else:
        messages.error(request, "This link has expired")
        return redirect("login")


def resetpassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm-Password"]

        if password == confirm_password:
            uid = request.session.get("uid")
            if uid:
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("login")
            else:
                messages.error(request, "Invalid session. Please try again.")
                return redirect("resetpassword")
        else:
            messages.error(request, "Passwords do not match.")
            return redirect("resetpassword")
    else:
        return render(request, "accounts/resetPassword.html")
