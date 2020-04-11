from ..core.utils import slugify


def upload_hero_photo(instance, filename: str) -> str:
    new_filename = slugify(instance.full_name)
    file_ext = filename.split('.')[-1]
    return f'coaches/hero/{new_filename}.{file_ext}'


def upload_main_photo(instance, filename: str) -> str:
    new_filename = slugify(instance.full_name)
    file_ext = filename.split('.')[-1]
    return f'coaches/main/{new_filename}.{file_ext}'
