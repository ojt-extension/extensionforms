# accounts/forms.py

from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import CustomUser

class OJTCoordinatorCreationForm(UserCreationForm):
    """
    A user creation form for OJT Coordinators with full name fields and
    @cvsu.edu.ph email domain validation.
    """
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True, help_text='Please use a @cvsu.edu.ph email.')
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)
        # Note: The username field is automatically handled by UserCreationForm.
        # We need to make sure the CustomUser model handles the username/email properly.

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@cvsu.edu.ph'):
            raise ValidationError("Please use a valid @cvsu.edu.ph email address.")
        return email


class OJTCoordinatorLoginForm(AuthenticationForm):
    """
    A custom authentication form that allows users to log in with their
    username and password, and properly handles validation.
    """
    username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter email or username'})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # We use the correct model manager to authenticate.
            # This handles both email and username as a login identifier if your backend supports it.
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return self.cleaned_data