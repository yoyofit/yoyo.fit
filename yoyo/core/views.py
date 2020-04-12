from io import BytesIO
from xml.etree import ElementTree
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import JsonResponse, HttpResponse
from django.templatetags.static import static


def site_index(request):
    return render(request, 'yoyo/index.html')


def manifest_view(request: HttpRequest):
    response = {
        'name': 'YoYo.fit',
        'icons': [
            {
                'src': static('yoyo/favicons/android-icon-36x36.png'),
                'size': '36x36',
                'type': 'image/png',
                'density': '0.75',
            },
            {
                'src': static('yoyo/favicons/android-icon-48x48.png'),
                'size': '48x48',
                'type': 'image/png',
                'density': '1.0',
            },
            {
                'src': static('yoyo/favicons/android-icon-72x72.png'),
                'size': '72x72',
                'type': 'image/png',
                'density': '1.5',
            },
            {
                'src': static('yoyo/favicons/android-icon-96x96.png'),
                'size': '96x96',
                'type': 'image/png',
                'density': '2.0',
            },
            {
                'src': static('yoyo/favicons/android-icon-144x144.png'),
                'size': '144x144',
                'type': 'image/png',
                'density': '3.0',
            },
            {
                'src': static('yoyo/favicons/android-icon-192x192.png'),
                'size': '192x192',
                'type': 'image/png',
                'density': '4.0',
            },
        ]
    }

    return JsonResponse(response)


def browser_config_view(request: HttpRequest):
    root = ElementTree.Element('browserconfig')
    app = ElementTree.Element('msapplication')
    tile = ElementTree.Element('tile')
    root.append(app)
    app.append(tile)

    square70x70logo = ElementTree.SubElement(tile, 'square70x70logo')
    square70x70logo.attrib = {
        'src': static('yoyo/favicons/ms-icon-70x70.png')
    }

    square150x150logo = ElementTree.SubElement(tile, 'square150x150logo')
    square150x150logo.attrib = {
        'src': static('yoyo/favicons/ms-icon-150x150.png')
    }

    square310x310logo = ElementTree.SubElement(tile, 'square310x310logo')
    square310x310logo.attrib = {
        'src': static('yoyo/favicons/ms-icon-310x310.png')
    }

    tile_color = ElementTree.SubElement(tile, 'TileColor')
    tile_color.text = '#ffffff'

    tree = ElementTree.ElementTree(root)
    f = BytesIO()
    tree.write(f, encoding='utf-8', xml_declaration=True)

    return HttpResponse(f.getvalue(), content_type='text/xml')
