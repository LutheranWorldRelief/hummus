"""
create custom clean template with data validation
"""
from django.utils.translation import gettext_lazy as _

from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.utils.cell import column_index_from_string

from .models import Project, Organization, Sex, Education, Country, Product, ContactType
from .common import get_localized_name as __


# creates catalog and validations
def create_catalog(book, request):

    dvs = {}
    sheet = book.create_sheet(__('catalog'))

    # catalog_cols = (Project, Organization, Sex, Educacion, Country, Departament, Comunity,
    # Product, ContactType)
    catalog_cols = (Project, Organization, Sex, Education, Country, Product, ContactType)
    col_start = 1
    row_start = 1
    for col, col_value in enumerate(catalog_cols, start=col_start):
        sheet.cell(row=row_start, column=col, value=col_value.__name__)
    row_start = 2
    for col, col_value in enumerate(catalog_cols, start=col_start):
        if hasattr(col_value.objects, 'for_user'):
            rows = col_value.objects.for_user(request.user).all()
        else:
            rows = col_value.objects.all()
        row = 0
        for row, row_value in enumerate(rows, start=row_start):
            name = __('name') if hasattr(row_value, __('name')) else 'name'
            sheet.cell(row=row, column=col, value=getattr(row_value, name))
        letter = get_column_letter(col)
        dvs[col_value.__name__] = DataValidation(
            type="list", allow_blank=True, showDropDown=False,
            formula1="%s!$%s$2:$%s$%s" % (__('catalog'), letter, letter, row), )
        col += 1


    # applies validations
    sheet = book[_('data')]
    validation_cols = {'A': 'Project', 'B': 'Organization', 'F': 'Sex', 'H': 'Education',
                       'M': 'Country', 'Q': 'Product'}
    row_start = 3
    row_max = 2000

    for letter in validation_cols:
        data_validation = dvs[validation_cols[letter]]
        col = column_index_from_string(letter)
        sheet.add_data_validation(data_validation)
        data_validation.add('%s%s:%s%s' % (letter, row_start, letter, row_max))

    return sheet
