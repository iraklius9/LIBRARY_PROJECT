from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'personal_number', 'birth_date', 'is_staff', 'is_user')

    def clean(self):
        cleaned_data = super().clean()
        is_staff = cleaned_data.get('is_staff')
        is_user = cleaned_data.get('is_user')
        if is_staff and is_user:
            raise forms.ValidationError("You cannot be both staff and user.")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')
