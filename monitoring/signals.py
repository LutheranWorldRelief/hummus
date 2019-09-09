from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.http import HttpResponse
from django.utils import translation
from monitoring.models import Profile
from django.conf import settings

@receiver(user_logged_in)
def on_login(sender, request, **kwargs):
    languageUser = Profile.objects.filter(user_id=request.user.id).values('language').first()
    if languageUser:
        translation.activate(languageUser['language'])
        request.session[translation.LANGUAGE_SESSION_KEY] = languageUser['language']
        response = HttpResponse()
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, languageUser['language'])
