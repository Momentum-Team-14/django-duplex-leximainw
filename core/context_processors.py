from django.conf import settings


def sitewide(request):
    return {
        'site_title': settings.SITE_TITLE,
        'site_name': settings.SITE_NAME,
    }
