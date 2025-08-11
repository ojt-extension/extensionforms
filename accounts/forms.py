# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import CustomUser

class OJTCoordinatorCreationForm(UserCreationForm):
    """
    Custom user creation form that handles email-based authentication
    and validates the @cvsu.edu.ph email domain.
    """
class OJTCoordinatorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',) # ADDED 'username'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@cvsu.edu.ph'):
            raise ValidationError("Please use a valid @cvsu.edu.ph email address.")
        return email
    
class OJTCoordinatorLoginForm(AuthenticationForm):
    # Change the field to a CharField to accept both emails and usernames
    username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    # The password field remains the same
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a placeholder for a better user experience
        self.fields['username'].widget.attrs['placeholder'] = 'Enter email or username'

    def clean(self):
        # Override the clean method to bypass default AuthenticationForm email validation
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                # The authentication will be handled in the view logic
                # So we just pass the cleaned data without raising an error here
                pass 
        return self.cleaned_data