# accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in
    using either their email or username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # The 'username' field on the form can be either an email or a username
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to avoid timing attacks
            UserModel().set_password(password)
            return None
        return None