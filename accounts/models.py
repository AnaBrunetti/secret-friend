from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from helpers.models import TimestampModel


class User(AbstractUser):
    ROLE_PROFESSIONAL = 'professional'
    ROLE_PATIENT = 'patient'
    ROLE_CHOICES = [
        (ROLE_PROFESSIONAL, _('Profissional')),
        (ROLE_PATIENT, _('Paciente'))
    ]
    
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_OTHER = 'other'
    GENDER_CHOICES = [
        (GENDER_MALE, _('Masculino')),
        (GENDER_FEMALE, _('Feminino')),
        (GENDER_OTHER, _('Outros')),
    ]
    
    role = models.CharField(
        verbose_name=_('role'),
        max_length=16,
        choices=ROLE_CHOICES
    )
    date_of_birth = models.DateField(
        verbose_name=_("Data de nascimento"),
        blank=True,
        null=True
    )
    gender = models.CharField(
        verbose_name=_("Gênero"),
        max_length=16,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Atualizado em"),
        auto_now=True
    )


class Profissional(TimestampModel):
    user = models.OneToOneField(
        verbose_name=_("Usuário"),
        to=User,
        related_name=_("profissional"),
        on_delete=models.CASCADE
    )
    phone = models.CharField(
        verbose_name=_("Número de telefone"),
        max_length=255,
        help_text=_("Exemplo de formato: (999) 99999-9999, (99) 9999-9999"),
        validators=[
            RegexValidator(regex="^\(\d{2,3}\) \d{4,5}\-\d{4}$", message="Número inválido", code="invalid_phone")
        ]
    )
    picture = models.ImageField(
        verbose_name=_("Foto de perfil"),
        upload_to="user/",
        max_length=255
    )
    document = models.FileField(
        verbose_name=_("Foto do documento"),
        upload_to="user/",
        max_length=255
    )
    crm = models.CharField(
        verbose_name=_("Número de CRM"),
        max_length=255,
        help_text=_("Exemplo de formato: 999999-XX"),
        validators=[
            RegexValidator(regex="^\d{2,6}-[A-Z]{2}$", message="CRM inválido", code="invalid_crm")
        ]
    )
    is_approved = models.BooleanField(
        verbose_name=_("Está Aprovado?"),
        default=False
    )
    
    class Meta:
        verbose_name = _("Profissional")
        verbose_name_plural = _("Profissionais")
        
    def __str__(self):
        return self.user.first_name