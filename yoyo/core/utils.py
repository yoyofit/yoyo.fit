from django.conf import settings
from django.utils.module_loading import import_string

YOYO_SLUGIFY = getattr(settings, 'YOYO_SLUGIFY', 'yoyo.core.slugify.default')

slugify = import_string(YOYO_SLUGIFY)

