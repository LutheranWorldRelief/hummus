"""
settings for django constance
"""
CONSTANCE_CONFIG = {
    'SALESFORCE_SYNC': (True, 'Salesforce Syncronization', bool),
    'SALESFORCE_FREQ': (60, 'Salesforce Syncronization Frequency in minutes', int),
    'START_ROW': (2, 'Data starts at this row', int),
}
