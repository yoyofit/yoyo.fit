import sys
from getpass import getpass
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import DEFAULT_DB_ALIAS, IntegrityError
from django.core.management.base import BaseCommand

from ...validators import validate_username, validate_email

User = get_user_model()


class NotRunningInTTYException(Exception):
    pass


class Command(BaseCommand):
    help = 'Used to create a superuser.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            dest='username',
            default=None,
            help='Specifies the username for the superuser.',
        )
        parser.add_argument(
            '--email',
            dest='email',
            default=None,
            help='Specifies the e-mail for the superuser.',
        )
        parser.add_argument(
            '--password',
            dest='password',
            default=None,
            help='Specifies the password for the superuser.',
        )
        parser.add_argument(
            '--noinput',
            '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help=(
                'Tells YoYo to NOT promt the user for input '
                'of any kind. You must user --username with '
                '--noinput, along with an option for any other '
                'required field. Superuser created with '
                '--noinput will not be able to log in until '
                'they\'re given a valid password.'
            ),
        )
        parser.add_argument(
            '--database',
            action='store',
            dest='database',
            default=DEFAULT_DB_ALIAS,
            help='Specifies the database to use. Default is "default".',
        )

    def execute(self, *args, **options):
        # Используется для тестирования
        self.stdin = options.get('stdin', sys.stdin)
        return super().execute(*args, **options)

    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')
        interactive = options.get("interactive")
        verbosity = int(options.get('verbosity', 1))

        if username is not None:
            try:
                username = username.strip()
                validate_username(username)
            except ValidationError as e:
                self.stderr.write('\n'.join(e.messages))

        if email is not None:
            try:
                email = email.strip()
                validate_email(email)
            except ValidationError as e:
                self.stderr.write('\n'.join(e.messages))

        if password is not None:
            password = password.strip()
            if password == '':
                self.stderr.write('Error: Blank passwords aren\'t allowed.')

        if not interactive:
            if username and email and password:
                self.create_superuser(username, email, password, verbosity)
        else:
            try:
                if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
                    raise NotRunningInTTYException('Not running in a TTY')

                while not username:
                    try:
                        raw_value = input('Enter displayed username: ').strip()
                        validate_username(raw_value)
                        username = raw_value
                    except ValidationError as e:
                        self.stderr.write('\n'.join(e.messages))

                while not email:
                    try:
                        raw_value = input('Enter e-mail address: ').strip()
                        validate_email(raw_value)
                        email = raw_value
                    except ValidationError as e:
                        self.stderr.write('\n'.join(e.messages))

                while not password:
                    raw_value = getpass('Enter password: ')
                    password_repeat = getpass('Repeat password: ')
                    if raw_value != password_repeat:
                        self.stderr.write('Error: Your password didn\'t match.')
                        continue
                    if raw_value.strip() == '':
                        self.stderr.write('Error: Blank password aren\'t allowed.')
                        continue
                    try:
                        validate_password(raw_value, user=User(username=username, email=email))
                    except ValidationError as e:
                        self.stderr.write('\n'.join(e.messages))
                        response = input('Bypass password validation and create user anyway? [y/N]: ')
                        if response.lower() != 'y':
                            continue
                    password = raw_value

                self.create_superuser(username, email, password, verbosity)
            except KeyboardInterrupt:
                self.stderr.write('\nOperation canceled.')
                sys.exit(1)
            except NotRunningInTTYException:
                self.stderr.write(
                    'Superuser creation skipped due to not running in a TTY. '
                    'You can run `manage.py createsuperuser` in your project '
                    'to create one manually.'
                )

    def create_superuser(self, username, email, password, verbosity):
        try:
            user = User.objects.create_superuser(username, email, password)
            if verbosity >= 1:
                message = 'Superuser #%s has been created successfully.'
                self.stderr.write(message % user.pk)
        except ValidationError as e:
            self.stderr.write(e.messages[0])
        except IntegrityError as e:
            self.stderr.write(e.messages[0])
