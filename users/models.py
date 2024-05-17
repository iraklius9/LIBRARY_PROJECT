from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=150)
    personal_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r'^\d{11}$', 'Personal number must be 11 digits.')]
    )
    birth_date = models.DateField(null=True, blank=False)

    is_staff = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'birth_date']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_user = True
        super().save(*args, **kwargs)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
