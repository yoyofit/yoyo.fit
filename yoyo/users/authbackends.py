from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class YoYoBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if kwargs.get('email'):
            username = kwargs['email']

        if not username or not password:
            return None

        try:
            user = User.objects.get_by_username_or_email(username)
        except User.DoesNotExist:
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
