from django.http import JsonResponse
from django.utils import translation as trans
from django.utils.translation import gettext_lazy as _


def get_localized_name(column):
    return column if trans.get_language() in ['en'] else column+'_'+trans.get_language()


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
