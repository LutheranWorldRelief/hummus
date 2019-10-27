"""
general system views
"""
import sys

from django.template import loader
from django.http import HttpResponseServerError


def server_error(request, template_name='500.html'):
    """ custom 500 handler, it add message """
    t = loader.get_template(template_name)
    etype, value, tb = sys.exc_info()
    return HttpResponseServerError(t.render({'exception_value': value,
                                             'exception_type': etype.__name__}))
