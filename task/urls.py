
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),

    path(
        "appointment/",
        views.appointment_view,
        name="appointment",
    ),
    path(
        "contact/",
        views.contact_view,
        name="contact",
    ),
    path(
        "track-appointment/",
        views.track_appointment_view,
        name="track_appointment",
    ),
    path(
        "appointment/success/<str:tracking_code>/",
        views.appointment_success_view,
        name="appointment_success",
    ),


    path(
    "send-client-email/",
    views.send_client_email,
    name="send_client_email",
    ),
]
