import os
import pyqrcode
from django.urls import reverse
from django.http.request import HttpRequest
from django.conf import settings
from .models import Coach


def generate_qr_code(instance: Coach, request: HttpRequest) -> str:
    save_path = os.path.join(settings.MEDIA_ROOT, 'coaches', 'qr')
    os.makedirs(save_path, exist_ok=True)
    svg_filename = 'id{}.svg'.format(instance.pk)

    if not os.path.isfile(os.path.join(save_path, svg_filename)):
        full_url = request.build_absolute_uri(reverse('yoyo:detail', kwargs={'pk': instance.pk}))
        qr = pyqrcode.create(full_url)
        qr.svg(os.path.join(save_path, svg_filename), scale=4)

    return '/'.join([settings.MEDIA_URL, 'coaches', 'qr', svg_filename])
