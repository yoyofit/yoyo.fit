from django.urls import re_path, path, include
from django.views.generic import TemplateView
from .core.views import site_index

app_name = 'yoyo'

urlpatterns = [
    path('', include('yoyo.coaches.urls')),
    path(
        'robots.txt',
        TemplateView.as_view(
            content_type='text/plain', template_name='yoyo/robots.txt'
        )
    ),
    re_path(r'^$', site_index, name='index')
]

# Регистрируем API

apiurlpatterns = [
    # path('', include('')),
]

urlpatterns += [path('api/', include((apiurlpatterns, 'api'), namespace='api'))]
