from django.conf import settings  # import the settings file


def admin_domain(request):
    # return the value you want as a dictionnary.
    return {'DOMAIN_SERVER': settings.DOMAIN_SERVER}
