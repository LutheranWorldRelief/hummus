import re
from functools import wraps

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Func, Value
from django.http import JsonResponse
from django.utils import translation
from django.utils.translation import gettext_lazy as _


def domain_required(function=None):

    def check_domain(user):
            # domain required
            domain = user.email.endswith('{}%s'.format(settings.MICROSOFT_DOMAIN) )

            # super user can always get int
            superuser = user.is_superuser

            # if you can view projects, you can view this...
            permission = user.has_perm('monitoring.project.can_view')

            return domain or superuser or permission

    return user_passes_test(check_domain)


class DomainRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        # domain required
        domain = self.request.user.email.endswith('{}%s'.format(settings.MICROSOFT_DOMAIN) )

        # super user can always get int
        superuser = self.request.user.is_superuser

        # if you can view projects, you can view this...
        permission = self.request.user.has_perm('monitoring.project.can_view')

        return domain or superuser or permission


def language_no_region(language):
    if '-' in language:
        language, _, region = language.lower().partition('-')
    return language


def get_localized_name(column):
    language = language_no_region(translation.get_language())
    default_language = language_no_region(settings.LANGUAGE_CODE)
    return column if language in default_language else "%s_%s" % (column, language)


def getPostArray(string, request):
    """
    evaluates POST array in the form varible[0]['name']='value'
    returns dictionary variable {0: {'name': 'value'}, 1: {'name': 'othervalue'} }
    """

    dictionary = {}
    for var in request:
        m = re.search("(\w+)\[(\d+)\]\[(\w+)\]", var)
        if m and m.group(1) == string:
            integer_index = m.group(2)
            sub_index = m.group(3)
            value = request.get(var)
            if not integer_index in dictionary:
                dictionary[integer_index] = {}
            dictionary[integer_index][sub_index] = value
    return dictionary


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


months = [('1', 'January'),
          ('2', _('February')),
          ('3', _('March')),
          ('4', _('April')),
          ('5', _('May')),
          ('6', _('June')),
          ('7', _('July')),
          ('8', _('August')),
          ('9', _('September')),
          ('10', _('October')),
          ('11', _('November')),
          ('12', _('December')), ]


# credit to https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/#jsonresponsemixin-example
class JSONResponseMixin:
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


# credit to https://code.djangoproject.com/ticket/28805
class RegexpReplace(Func):
    function = 'REGEXP_REPLACE'

    def __init__(self, expression, pattern, replacement, flags, **extra):
        if not hasattr(flags, 'resolve_expression'):
            if not isinstance(flags, str):
                raise TypeError("'flags' must be a string")
            flags = Value(flags)
        if not hasattr(pattern, 'resolve_expression'):
            if not isinstance(pattern, str):
                raise TypeError("'pattern' must be a string")
            pattern = Value(pattern)
        if not hasattr(replacement, 'resolve_expression'):
            if not isinstance(replacement, str):
                raise TypeError("'replacement' must be a string")
            replacement = Value(replacement)
        expressions = [expression, pattern, replacement, flags]
        super().__init__(*expressions, **extra)
