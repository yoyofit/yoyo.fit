from django.shortcuts import render


def site_index(request):
    return render(request, 'yoyo/index.html')
