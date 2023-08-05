from django.utils import timezone
from django.db import models


class Token(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active'
        INACTIVE = 'inactive'
        BURNED = 'burned'

    category = models.CharField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True, default='')
    symbol = models.CharField(max_length=100)
    decimals = models.PositiveIntegerField(default=0)
    icon = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    class Meta:
        ordering = ('name', )


class Registry(models.Model):
    major = models.PositiveIntegerField(default=0) # incremented when an identity is removed
    minor = models.PositiveIntegerField(default=0) # incremented when an identity is added
    patch = models.PositiveIntegerField(default=0) # incremented when an identity is modified
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    latest_revision = models.DateTimeField(default=timezone.now)
    tokens = models.ManyToManyField(Token)

    class Meta:
        verbose_name_plural = 'Registries'
