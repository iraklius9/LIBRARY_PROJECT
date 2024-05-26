from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=150)
    personal_number = models.CharField(
        _('personal number'),
        max_length=11,
        unique=True,
        validators=[RegexValidator(r'^\d{11}$', _('Personal number must be 11 digits.'))]
    )
    birth_date = models.DateField(_('birth date'), null=True, blank=False)

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_user = models.BooleanField(_('user status'), default=False)

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
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=_('groups')
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions')
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
