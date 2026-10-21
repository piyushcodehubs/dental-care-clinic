
from django.contrib import admin
from .models import Appointment, ContactMessage


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "tracking_code",
        "dental_service",
        "preferred_date",
        "preferred_time",
        "status",
    )

    list_filter = ("status", "dental_service", "preferred_date")

    search_fields = (
        "full_name",
        "email",
        "phone_number",
        "tracking_code",
    )

    list_editable = ("status",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "subject",
        "is_read",
        "created_at",
    )

    list_filter = ("is_read", "created_at")
    search_fields = ("full_name", "email", "subject")
