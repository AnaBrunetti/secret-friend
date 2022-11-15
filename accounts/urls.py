from django.urls import path
from django.contrib.auth import views
from accounts.views import (
    CutomLoginView,
    RegisterView,
    ProfissionaRegisterView,
    PasswordChangeView,
    ProfessionalEditView,
    PatientEditView,
)


urlpatterns = [
    path('login/', CutomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    path("register", RegisterView.as_view(), name="register"),
    path("profissiona-register", ProfissionaRegisterView.as_view(), name="profissiona_register"),

    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path("professional_edit_profile/", ProfessionalEditView.as_view(), name="professional_edit_profile"),
    path("patient_edit_profile/", PatientEditView.as_view(), name="patient_edit_profile"),
]