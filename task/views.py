
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import AppointmentForm, ContactMessageForm
from .models import Appointment


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


def appointment_view(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save()

            return redirect(
                "appointment_success",
                tracking_code=appointment.tracking_code,
            )

        messages.error(
            request,
            "Please correct the errors in your appointment form."
        )
    else:
        form = AppointmentForm()

    return render(
        request,
        "appointment.html",
        {"form": form},
    )


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
