from django import forms
from django.utils import timezone

from .models import Appointment, ContactMessage


class AppointmentForm(forms.Form):
    name = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()
    service = forms.ChoiceField(
        choices=Appointment.SERVICE_CHOICES
    )
    date = forms.DateField(
        input_formats=["%Y-%m-%d"]
    )
    time = forms.ChoiceField(
        choices=Appointment.TIME_CHOICES
    )
    message = forms.CharField(
        max_length=1000,
        required=False,
        strip=True,
        widget=forms.Textarea,
    )

    def clean_date(self):
        appointment_date = self.cleaned_data["date"]

        if appointment_date < timezone.localdate():
            raise forms.ValidationError(
                "Please select today or a future date."
            )

        return appointment_date

    def save(self):
        data = self.cleaned_data

        return Appointment.objects.create(
            full_name=data["name"],
            phone_number=data["phone"],
            email=data["email"],
            dental_service=data["service"],
            preferred_date=data["date"],
            preferred_time=data["time"],
            additional_information=data["message"],
        )


class ContactMessageForm(forms.Form):
    name = forms.CharField(max_length=150)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(
        max_length=5000,
        strip=True,
        widget=forms.Textarea,
    )

    def save(self):
        data = self.cleaned_data

        return ContactMessage.objects.create(
            full_name=data["name"],
            email=data["email"],
            subject=data["subject"],
            message=data["message"],
        )




from django import forms
from .models import Appointment


class ClientEmailForm(forms.Form):
    appointment = forms.ModelChoiceField(
        queryset=Appointment.objects.all(),
        label="Select patient appointment",
    )

    subject = forms.CharField(
        max_length=200,
        label="Email subject",
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 8,
            "placeholder": "Write your message to the patient...",
        }),
        max_length=10000,
        label="Your message",
    )
