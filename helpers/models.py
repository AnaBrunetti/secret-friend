from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimestampModelQueryset(models.QuerySet):
    def actives(self):
        return self.filter(is_active=True)


class TimestampModel(models.Model):
    """
        Extend this model if you wish to have automatically updated
        created_at and updated_at fields.
    """

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name=_("Criado em"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Atualizado em"),
        auto_now=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Ativo"),
        default=True,
        db_index=True,
        help_text=_("Este registro está ativo?")
    )

    # Manager
    objects = TimestampModelQueryset.as_manager()

    def save(self, *args, **kwargs):
        if kwargs.get("update_fields"):
            kwargs["update_fields"] = list(set(list(kwargs["update_fields"]) + ["updated_at"]))
        return super().save(*args, **kwargs)