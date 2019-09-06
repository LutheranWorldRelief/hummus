from django.utils import translation as trans

def get_localized_name(column):
    return column if trans.get_language() in ['en'] else column+'_'+trans.get_language()


