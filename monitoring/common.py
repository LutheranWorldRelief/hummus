"""
common or frequently used tools
"""

import re
import datetime

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Func, Value
from django.http import JsonResponse
from django.utils import translation
from django.utils.translation import gettext_lazy as _


def smart_assign(a, b):
    if b:
        a = b
    return a

def domain_required():
    def check_domain(user):
        # domain required
        domain = user.email.endswith('{}%s'.format(settings.MICROSOFT_DOMAIN))

        # super user can always get int
        superuser = user.is_superuser

        # if you can view projects, you can view this...
        permission = user.has_perm('monitoring.view_project')

        return domain or superuser or permission

    return user_passes_test(check_domain)


class DomainRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        # domain required
        domain = self.request.user.email.endswith('{}%s'.format(settings.MICROSOFT_DOMAIN))

        # super user can always get int
        superuser = self.request.user.is_superuser

        # if you can view projects, you can view this...
        permission = self.request.user.has_perm('monitoring.view_project')

        return domain or superuser or permission


def language_no_region(language):
    if '-' in language:
        language = language.lower().partition('-')[0]
    return language


def get_localized_name(column, language=None):
    default_language = language_no_region(settings.LANGUAGE_CODE)
    if not language:
        language = language_no_region(translation.get_language())
    return column if language in default_language else "%s_%s" % (column, language)


def get_post_array(string, request):
    """
    evaluates POST array in the form varible[0]['name']='value'
    returns dictionary variable {0: {'name': 'value'}, 1: {'name': 'othervalue'} }
    """

    dictionary = {}
    for var in request:
        match = re.search(r"(\w+)\[(\w+)\]", var)
        if match and match.group(1) == string:
            index = match.group(2)
            value = request.get(var)
            if index not in dictionary:
                dictionary[index] = value
    return dictionary


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


MONTHS = [('1', 'January'),
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


class JSONResponseMixin:
    """
    A mixin that can be used to render a JSON response.
    credit to
    https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/#jsonresponsemixin-example
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


def xstr(s):
    """ return empty instead of None. credit to https://stackoverflow.com/a/1034598/1170404 """
    return '' if s is None else str(s)


def parse_date(string, date_format=None):
    """ parses date in all possible formats, tries optional date_format first """

    # already date, return
    if isinstance(string, datetime.datetime):
        return string.date()
    if isinstance(string, datetime.date):
        return string

    # fixes date_format
    date_format_maps = {'m/d/Y': '%m/%d/%Y', 'd/m/Y': '%d/%m/%Y', 'Y-m-d': '%Y-%m-%d'}
    if date_format in date_format_maps:
        date_format = date_format_maps[date_format]

    # do parse
    date_formats = settings.DATE_INPUT_FORMATS
    date_formats.extend(settings.DATETIME_INPUT_FORMATS)
    if date_format:
        date_formats.insert(0, date_format)
    for fmt in date_formats:
        try:
            return datetime.datetime.strptime(str(string), fmt).date()
        except ValueError:
            pass
    return


class RegexpReplace(Func):
    """
    PostgreSQL Regex function for Django
    based on https://code.djangoproject.com/ticket/28805
    """
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
