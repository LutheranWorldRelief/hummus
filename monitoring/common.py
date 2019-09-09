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
