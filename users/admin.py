from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'is_staff', 'is_user', 'personal_number', 'birth_date')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
         {'fields': ('username', 'first_name', 'last_name', 'personal_number', 'birth_date', 'is_staff', 'is_user')}),
        ('Permissions', {'fields': ('is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'username', 'is_staff', 'is_user', 'personal_number', 'birth_date'),
        }),
    )

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_user')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
