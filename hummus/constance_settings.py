"""
settings for django constance
"""
CONSTANCE_CONFIG = {
    'SALESFORCE_SYNC': (True, 'Salesforce Syncronization', bool),
    'SALESFORCE_FREQ': (60, 'Salesforce Syncronization Frequency in minutes', int),
    'HEADER_ROW': (2, 'Row', int),
    'START_ROW': (3, 'Data starts at this row', int),
    'LOCATION_FIELD': ('location', 'Location field name', str),
    'MDC_HEADER_PREFIX': ('form.', 'Prefix for MDC headers in Excel', str),
    'DEFAULT_TEMPLATE': ('clean-template', 'Default template ID', str),
    'ALLOW_INVALID_IMPORT': (False, 'Import with Invalid Data', bool),
}
