
import re
from threading import Thread

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    AppointmentForm,
    ContactMessageForm,
    ClientEmailForm,
)
from .models import Appointment
from .email_utils import send_appointment_confirmation


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

def home(request):
    return render(request, "home.html")


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

def about(request):
    return render(request, "about.html")


# --------------------------------------------------
# SERVICES PAGE
# --------------------------------------------------

def services(request):
    return render(request, "services.html")


# --------------------------------------------------
# EMAIL VALIDATION
# --------------------------------------------------

def is_valid_email_address(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


# --------------------------------------------------
# INDIAN MOBILE NUMBER VALIDATION
# Accepts:
# 9876543210
# +919876543210
# +91 98765 43210
# 919876543210
# --------------------------------------------------

def is_valid_indian_mobile(phone):
    value = re.sub(r"[\s()-]", "", phone or "")

    if value.startswith("+91"):
        value = value[3:]
    elif value.startswith("91") and len(value) == 12:
        value = value[2:]

    return bool(re.fullmatch(r"[6-9]\d{9}", value))


# --------------------------------------------------
# SEND APPOINTMENT EMAIL IN BACKGROUND
# --------------------------------------------------

def send_email_in_background(appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        send_appointment_confirmation(appointment)

    except Exception as error:
        print(f"EMAIL ERROR: {error}")


# --------------------------------------------------
# APPOINTMENT BOOKING
# --------------------------------------------------

def appointment_view(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email", "").strip()
            phone = form.cleaned_data.get("phone", "").strip()

            # Validate email on the server.
            if not is_valid_email_address(email):
                form.add_error(
                    "email",
                    "Please enter a valid email address."
                )

            # Validate Indian mobile number on the server.
            if not is_valid_indian_mobile(phone):
                form.add_error(
                    "phone",
                    "Enter a valid 10-digit Indian mobile number."
                )

            # Only save and send email if all validation passes.
            if not form.errors:
                appointment = form.save()

                Thread(
                    target=send_email_in_background,
                    args=(appointment.id,),
                    daemon=True,
                ).start()

                return redirect(
                    "appointment_success",
                    tracking_code=appointment.tracking_code,
                )

        messages.error(
            request,
            "Please correct the errors highlighted in your form."
        )

    else:
        form = AppointmentForm()

    return render(
        request,
        "appointment.html",
        {"form": form},
    )


# --------------------------------------------------
# CONTACT FORM
# --------------------------------------------------

def contact_view(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Thank you for contacting us. Your message has been sent."
            )

            return redirect("contact")

        messages.error(
            request,
            "Please correct the errors in your contact form."
        )

    else:
        form = ContactMessageForm()

    return render(
        request,
        "contact.html",
        {"form": form},
    )


# --------------------------------------------------
# TRACK APPOINTMENT
# --------------------------------------------------

def track_appointment_view(request):
    appointment = None
    error = None

    if request.method == "POST":
        tracking_code = request.POST.get(
            "tracking_code", ""
        ).strip().upper()

        if tracking_code:
            appointment = Appointment.objects.filter(
                tracking_code=tracking_code
            ).first()

        if appointment is None:
            error = (
                "No appointment was found with that tracking code. "
                "Please check the code and try again."
            )

    return render(
        request,
        "track_appointment.html",
        {
            "appointment": appointment,
            "error": error,
        },
    )


# --------------------------------------------------
# APPOINTMENT SUCCESS PAGE
# --------------------------------------------------

def appointment_success_view(request, tracking_code):
    appointment = get_object_or_404(
        Appointment,
        tracking_code=tracking_code,
    )

    return render(
        request,
        "appointment_success.html",
        {"appointment": appointment},
    )


# --------------------------------------------------
# STAFF: SEND EMAIL TO A CLIENT
# --------------------------------------------------

@staff_member_required
def send_client_email(request):
    if request.method == "POST":
        form = ClientEmailForm(request.POST)

        if form.is_valid():
            appointment = form.cleaned_data["appointment"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[appointment.email],
                    fail_silently=False,
                )

                messages.success(
                    request,
                    f"Email sent to {appointment.email}.",
                )

                return redirect("send_client_email")

            except Exception:
                messages.error(
                    request,
                    "Email could not be sent. Check your email settings.",
                )

    else:
        form = ClientEmailForm()

    return render(
        request,
        "send_client_email.html",
        {"form": form},
    )
