from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone


def send_appointment_confirmation(appointment):
    booking_time = timezone.localtime(appointment.created_at)

    subject = "Your Dental Appointment Request"

    message = f"""
Hello {appointment.full_name},

Thank you for booking with DentalCare!

Tracking Code: {appointment.tracking_code}
Dental Service: {appointment.get_dental_service_display()}
Preferred Date: {appointment.preferred_date}
Preferred Time: {appointment.get_preferred_time_display()}
Status: {appointment.get_status_display()}
Booking Submitted At: {booking_time.strftime("%d %B %Y, %I:%M %p")}

Thank you,
DentalCare Team
"""

    return send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.email],
        fail_silently=False,
    )