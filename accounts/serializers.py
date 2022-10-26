

from rest_framework import serializers
from rest_auth.serializers import LoginSerializer
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

from accounts.models import (
    User,
    Profissional,
)

User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["email", "password"]


class CustomRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField()
    # contact_number = serializers.CharField()
    # address = serializers.CharField(required=False)
    # city = serializers.CharField(required=False)
    # state = serializers.CharField(required=False)
    # postal_code = serializers.CharField(required=False)
    # role = serializers.ChoiceField(choices=[User., User.ROLE_CLINICIAN])
    # date_of_birth = serializers.DateField(required=True)

    # def validate(self, data):
    #     super().validate(data)
    #     email = data.get('email')
    #     if not validate_email_domain(email):
    #         raise ValidationError({'email': _('Invalid e-mail domain.')})
    #     return data

    # def get_cleaned_data(self):
    #     return {
    #         'username': self.validated_data.get('username', ''),
    #         'password1': self.validated_data.get('password1', ''),
    #         'first_name': self.validated_data.get('first_name', ''),
    #         'last_name': self.validated_data.get('last_name', ''),
    #         'contact_number': self.validated_data.get('contact_number', ''),
    #         'address': self.validated_data.get('address', ''),
    #         'city': self.validated_data.get('city', ''),
    #         'state': self.validated_data.get('state', ''),
    #         'postal_code': self.validated_data.get('postal_code', ''),
    #         'email': self.validated_data.get('email', ''),
    #         'role': self.validated_data.get('role', ''),
    #         'date_of_birth': self.validated_data.get('date_of_birth', '')
    #     }

    # def save(self, request):
    #     adapter = get_adapter()
    #     user = adapter.new_user(request)
    #     self.cleaned_data = self.get_cleaned_data()
    #     adapter.save_user(request, user, self, commit=False)
    #     self.custom_signup(request, user)
    #     user = User.objects.get(id=user.id)
    #     setup_user_email(request, user, [])
    #     return user

    # def custom_signup(self, request, user):
    #     with transaction.atomic():
    #         user.email = user.email.lower()
    #         user.username = user.email
    #         user.identity = generate_identity(user.email)
    #         user.contact_number = self.cleaned_data.get('contact_number')
    #         user.address = self.cleaned_data.get('address')
    #         user.city = self.cleaned_data.get('city')
    #         user.state = self.cleaned_data.get('state')
    #         user.postal_code = self.cleaned_data.get('postal_code')
    #         user.role = self.cleaned_data.get('role')
    #         user.date_of_birth = self.cleaned_data.get('date_of_birth') 
    #         user.has_reset_password = True
    #         user.save()

    #         if user.is_clinician:
    #             profile = ClinicianProfile.objects.create(user=user, name=f'{user.get_full_name()}')
    #         else:
    #             profile = BattleBuddyProfile.objects.create(user=user, name=f'{user.get_full_name()}')

    #         LeadManager(profile).register()


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "date_of_birth", "picture", "last_login"]
        read_only_fields = ["id", "email", "last_login"]
