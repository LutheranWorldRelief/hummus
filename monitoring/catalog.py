from django.utils.translation import gettext_lazy as _

from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string

from .models import *
from .common import get_localized_name as __


# creates catalog and validations
def create_catalog(wb, request):

    dvs = {}
    ws = wb.create_sheet(__('catalog'))

    # catalog_cols = (SubProject, Organization, Sex, Educacion, Country, Departament, Comunity, Product, ContactType) TODO: qué pasó con Departamento y Comunity?
    catalog_cols = (SubProject, Organization, Sex, Education, Country, Product, ContactType)
    col_start = 1
    row_start = 1
    for col, col_value in enumerate(catalog_cols, start=col_start):
        ws.cell(row=row_start, column=col, value=col_value.__name__)
    row_start = 2
    for col, col_value in enumerate(catalog_cols, start=col_start):
        if hasattr(col_value.objects, 'for_user'):
            rows = col_value.objects.for_user(request.user).all()
        else:
            rows = col_value.objects.all()
        for row, row_value in enumerate(rows, start=row_start):
            ws.cell(row=row, column=col, value=getattr(row_value, __('name')))
        letter = get_column_letter(col)
        dvs[col_value.__name__] = DataValidation(type="list", allow_blank=True, showDropDown=False, formula1="catalog!$%s$2:$%s$%s" % (letter, letter, row), )
        col += 1


    # applies validations
    ws = wb.get_sheet_by_name(_('data'))
    ws = wb.active
    validation_cols = {'A': 'SubProject', 'B': 'Organization', 'F': 'Sex', 'H': 'Education', 'M': 'Country', 'Q': 'Product'}
    row_start = 3
    row_max = 2000

    for letter in validation_cols:
        dv = dvs[validation_cols[letter]]
        col = column_index_from_string(letter)
        ws.add_data_validation(dv)
        dv.add('%s%s:%s%s' % (letter, row_start, letter, row_max))

    return ws
