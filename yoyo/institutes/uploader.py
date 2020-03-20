from ..core.utils import slugify


def upload_logo(instance, filename: str) -> str:
    file_ext = filename.split('.')[-1]
    new_filename = slugify(instance.name)
    return f'institutes/logos/{new_filename}.{file_ext}'
