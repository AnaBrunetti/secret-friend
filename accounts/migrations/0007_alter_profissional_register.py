# Generated by Django 3.2.16 on 2022-11-16 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20221116_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profissional',
            name='register',
            field=models.CharField(default=1, help_text='Exemplo de formato: 999999', max_length=255, verbose_name='Número de registro'),
            preserve_default=False,
        ),
    ]
