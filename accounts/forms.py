from django import forms
from django.forms import ValidationError
from django.forms.models import fields_for_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _

from accounts.models import User, Profissional


class CustomUserForm(AuthenticationForm):
    
    def confirm_login_allowed(self, user):
        if user.role == User.ROLE_PROFESSIONAL and not user.profissional.is_approved:
            self.add_error("username", "Profissional pendente de aprovação.")
        return super(CustomUserForm, self).confirm_login_allowed(user)


class RegisterForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['username'].widget.attrs['disabled'] = True
        self.fields['gender'].required = True
        self.fields['gender'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'date_of_birth', 'gender', 'role', 'password1', 'password2']
        widgets = {
            'role': forms.HiddenInput(),
            'gender': forms.Select(),
        }


class ProfissionalRegisterForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_('Enter the same password as before, for verification.'),
    )

    def __init__(self, *args, **kwargs):
        _fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'gender', 'role']
        super(ProfissionalRegisterForm, self).__init__(*args, **kwargs)
        self.fields.update(fields_for_model(User, _fields))
        self.fields['role'].widget = forms.HiddenInput()
        self.fields['gender'].required = True
        for field in self.fields:
            if self.fields[field] and hasattr(self.fields[field], 'widget') and hasattr(self.fields[field].widget, 'attrs'):    
                self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['placeholder'] = "(99) 9999-9999"
        self.fields['cpf'].widget.attrs['placeholder'] = "999.999.999-99"
        self.fields['date_of_birth'].widget.attrs['type'] = "date"
        

    class Meta:
        model = Profissional
        exclude = ['user', 'is_approved']
        widgets = {
            'gender': forms.Select(),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True, is_approved=False, *args, **kwargs):
        user_fields = {
            "first_name": self.cleaned_data['first_name'],
            "last_name": self.cleaned_data['last_name'],
            "date_of_birth": self.cleaned_data['date_of_birth'],
            "gender" : self.cleaned_data['gender'],
            "role": self.cleaned_data['role'],
        }
        user = User.objects.create_user(
            username = self.cleaned_data['username'],
            password = self.cleaned_data['password1'],
            **user_fields
        )
        profissional = super(ProfissionalRegisterForm, self).save(commit=False)
        profissional.user = user
        profissional.is_approved = is_approved
        if commit:
            profissional.save()
        return profissional


class PatientEditForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['username'].widget.attrs['disabled'] = True
        self.fields['gender'].required = True
        self.fields['gender'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'date_of_birth', 'gender']
        widgets = {
            'role': forms.HiddenInput(),
            'gender': forms.Select(),
        }