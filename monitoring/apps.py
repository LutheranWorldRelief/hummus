from django.apps import AppConfig
from django.apps import AppConfig
from .signals import *

class MonitoringConfig(AppConfig):
    name = 'monitoring'

    def ready(self):
        on_login