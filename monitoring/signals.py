from django.dispatch import receiver

#<<Start Config language >>
from django.contrib.auth.signals import user_logged_in
from django.http import HttpResponse
from django.utils import translation
from monitoring.models import Profile
from hummus import settings;

@receiver(user_logged_in)
def on_login(sender, request, **kwargs):
    languageUser = Profile.objects.filter(user_id=request.user.id).values('language')

    if languageUser:
        translation.activate(languageUser[0]['language'])
        response = HttpResponse(...)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, languageUser[0]['language'])
#<<End Config language >>
