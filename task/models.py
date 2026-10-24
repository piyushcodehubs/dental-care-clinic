
from django.db import models, IntegrityError, transaction
import secrets


class Appointment(models.Model):

    SERVICE_CHOICES = [
        ("general", "General Dentistry"),
        ("checkup", "Dental Checkup"),
        ("whitening", "Teeth Whitening"),
        ("braces", "Braces and Alignment"),
        ("root_canal", "Root Canal Treatment"),
        ("children", "Children's Dentistry"),
        ("implants", "Dental Implants"),
        ("other", "Other"),
    ]

    TIME_CHOICES = [
        ("09:00", "9:00 AM"),
        ("10:00", "10:00 AM"),
        ("11:00", "11:00 AM"),
        ("12:00", "12:00 PM"),
        ("13:00", "1:00 PM"),
        ("14:00", "2:00 PM"),
        ("15:00", "3:00 PM"),
        ("16:00", "4:00 PM"),
        ("17:00", "5:00 PM"),
        ("18:00", "6:00 PM"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    dental_service = models.CharField(
        max_length=30,
        choices=SERVICE_CHOICES,
    )

    preferred_date = models.DateField()

    preferred_time = models.CharField(
        max_length=5,
        choices=TIME_CHOICES,
    )

    additional_information = models.TextField(
        blank=True,
        max_length=1000,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    tracking_code = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        editable=False,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.preferred_date}"

    def save(self, *args, **kwargs):
        # Generate a tracking code for new appointments
        if not self.tracking_code:
            for _ in range(5):
                self.tracking_code = (
                    "DC-" + secrets.token_hex(6).upper()
                )

                try:
                    with transaction.atomic():
                        return super().save(*args, **kwargs)

                except IntegrityError:
                    # Retry if the tracking code already exists
                    self.tracking_code = ""

            raise RuntimeError(
                "Could not generate a unique appointment tracking code."
            )

        return super().save(*args, **kwargs)


class ContactMessage(models.Model):

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=5000)

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} - {self.full_name}"
