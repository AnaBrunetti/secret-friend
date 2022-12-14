# Generated by Django 3.2.16 on 2022-11-15 07:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='profissional',
            name='cpf',
            field=models.CharField(default='446.929.028-92', help_text='Exemplo de formato: 999.999.999-99', max_length=255, validators=[django.core.validators.RegexValidator(code='invalid_cpf', message='CRM inválido', regex='^\\d{3}.\\d{3}.\\d{3}-\\d{2}$')], verbose_name='CPF'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profissional',
            name='crm',
            field=models.CharField(blank=True, help_text='Exemplo de formato: 999999-XX', max_length=255, null=True, validators=[django.core.validators.RegexValidator(code='invalid_crm', message='CRM inválido', regex='^\\d{2,6}-[A-Z]{2}$')], verbose_name='Número de CRM'),
        ),
    ]
