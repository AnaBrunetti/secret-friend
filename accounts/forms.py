from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class RegisterForm(UserCreationForm):

	class Meta:
		model = User
		fields = ["username", "date_of_birth", "gender", "password1", "password2"]
