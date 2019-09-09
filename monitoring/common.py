from django.utils import translation as trans

def get_localized_name(column):
    return column if trans.get_language() in ['en'] else column+'_'+trans.get_language()


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


