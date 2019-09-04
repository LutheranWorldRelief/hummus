from django.conf import settings  # import the settings file


def legacy_url(request):
    return {'LEGACY_URL': settings.LEGACY_URL}
