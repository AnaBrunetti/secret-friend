from django.conf.urls import url, include
from rest_framework import routers
from rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    # PasswordResetView,
    # PasswordResetConfirmView
)
from rest_auth.registration.views import RegisterView
from accounts.views import (
    UserDetailsView,
    # UserAddressesView
)

""" Main router """
router = routers.SimpleRouter()
# router.register("addresses", UserAddressesView, basename="user_addresses")

urlpatterns = [
    # url(r"^password/reset/$", PasswordResetView.as_view(), name="password_reset"),
    # url(r"^password/reset/confirm/$", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    url(r"^login/$", LoginView.as_view(), name="account_login"),
    url(r"^registration/$", RegisterView.as_view(), name="account_signup"),

    # URLs that require a user to be logged in with a valid session / token.
    url(r"^logout/$", LogoutView.as_view(), name="account_logout"),
    url(r"^user/$", UserDetailsView.as_view(), name="user_details"),
    url(r"^password/change/$", PasswordChangeView.as_view(), name="password_change"),
    url(r"^user/", include(router.urls)),
]
