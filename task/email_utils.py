
from django.conf import settings
from django.core.mail import send_mail


def send_appointment_confirmation(appointment):
    subject = "Your Dental Appointment Request"

    message = f"""
Hello {appointment.full_name},

Thank you for booking with DentalCare!

Your appointment request details:

Tracking Code: {appointment.tracking_code}
Dental Service: {appointment.get_dental_service_display()}
Preferred Date: {appointment.preferred_date}
Preferred Time: {appointment.get_preferred_time_display()}
Status: {appointment.get_status_display()}

Please keep your tracking code to check your appointment status.

We will notify you when your appointment is confirmed.

Thank you,
DentalCare Team
"""

    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [appointment.email],
        fail_silently=False,
    )
