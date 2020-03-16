from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..core.utils import slugify
from .utils import hash_email


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('User must have username')
        if not email:
            raise ValueError('User must have email')

        user = self.model(**extra_fields)
        user.set_username(username)
        user.set_email(email)
        user.set_password(password)

        now = timezone.now()
        user.last_login = now
        user.joined_on = now

        user.save(using=self._db)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(username, email, password, **extra_fields)

    def get_by_username(self, username):
        return self.get(slug=slugify(username))

    def get_by_email(self, email):
        return self.get(email_hash=hash_email(email))

    def get_by_username_or_email(self, login):
        if '@' in login:
            return self.get(email_hash=hash_email(login))
        return self.get(slug=slugify(login))


class User(AbstractBaseUser, PermissionsMixin):
    # Мы даём возможность пользователю писать логин таким образом,
    # каким он его себе представляет, поэтому авторизацию будет проходить по другому полю,
    # регистронезависимому.
    username = models.CharField(max_length=30)
    slug = models.CharField(max_length=30, unique=True)

    # Электропочта пользователя также сохраняем в том виде, в каком хочет сам пользователь,
    # а авториизацию и поиск по электропочте будет по негистронезависимому полю,
    # свободного от всех пользовательских извращений.
    email = models.EmailField(_('E-mail'), max_length=255, db_index=True)
    email_hash = models.CharField(max_length=32, unique=True)

    first_name = models.CharField(_('First name'), max_length=60, null=True, blank=True)
    last_name = models.CharField(_('Last name'), max_length=120, null=True, blank=True)
    second_name = models.CharField(_('Second name'), max_length=60, null=True, blank=True)

    joined_on = models.DateTimeField(_('Joined on'), default=timezone.now)
    joined_from_ip = models.GenericIPAddressField(null=True, blank=True)

    is_staff = models.BooleanField(_('Staff status'), default=False)

    USERNAME_FIELD = 'slug'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        if self.get_full_name:
            return self.get_full_name
        return self.email

    @property
    def get_full_name(self):
        full_name = list()
        if self.second_name:
            full_name.append(self.second_name)
        if self.first_name:
            full_name.insert(0, self.first_name)
        if self.last_name:
            full_name.insert(0, self.last_name)
        return ' '.join(full_name)

    def set_username(self, new_username, changed_by=None):
        new_username = self.normalize_username(new_username)
        if new_username != self.username:
            old_username = self.username
            self.username = new_username
            self.slug = slugify(new_username)

            if self.pk:
                # TODO: сделать систему контроля измнения логинов
                changed_by = changed_by or self

    def set_email(self, new_email):
        self.email = UserManager.normalize_email(new_email)
        self.email_hash = hash_email(new_email)
