from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'full_name', 'personal_number', 'birth_date')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'username', 'full_name', 'personal_number', 'birth_date',
                'is_staff'),
        }),
    )

    list_display = ('email', 'username', 'full_name', 'is_staff', 'is_user', 'personal_number')
    search_fields = ('email', 'username', 'full_name', 'personal_number')
    ordering = ('birth_date',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['is_staff'].required = True
        return form

    def save_model(self, request, obj, form, change):
        if obj.is_staff:
            obj.is_user = False
        obj.save()


admin.site.register(CustomUser, CustomUserAdmin)
