# Generated by Django 3.2.16 on 2022-11-12 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profissional_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='profissional',
            name='picture',
            field=models.ImageField(default='', max_length=255, upload_to='user/', verbose_name='Foto de perfil'),
            preserve_default=False,
        ),
    ]