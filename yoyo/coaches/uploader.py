from datetime import date
from django.utils.crypto import get_random_string
from unidecode import unidecode
from yoyo.coaches.models import Coach


def upload_main_photo(instance: Coach, filename: str) -> str:
    today = date.today()
    new_filename = '{}_{}-{}_{}_{}'.format(today.year, today.month, new)
    file_ext = filename.split('.')[-1]
    return f'coach/main/{new_filename}.{file_ext}'
