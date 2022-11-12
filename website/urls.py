from django.urls import path
from website.views import (
    HomeView,
    AboutView,
    ContactView,
    TermsView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("terms/", TermsView.as_view(), name="terms"),
    path("contact/", ContactView.as_view(), name="contact"),
]