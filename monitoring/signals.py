"""
app signals for 'monitoring', called by AppConfig in apps.py
"""
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.http import HttpResponse
from django.utils import translation
from django.conf import settings

from monitoring.models import Profile

@receiver(user_logged_in)
def on_login(sender, request, **kwargs):
    language_user = Profile.objects.filter(user_id=request.user.id).values('language').first()
    if language_user:
        translation.activate(language_user['language'])
        request.session[translation.LANGUAGE_SESSION_KEY] = language_user['language']
        response = HttpResponse()
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_user['language'])
