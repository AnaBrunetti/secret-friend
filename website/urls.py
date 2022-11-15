from django.urls import path
from website.views import (
    AboutView,
    ContactView,
    TermsView,
)


urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
    path("terms/", TermsView.as_view(), name="terms"),
    path("contact/", ContactView.as_view(), name="contact"),
]