"""
Application configuration for 'monitoring'
"""
from django.apps import AppConfig


class MonitoringConfig(AppConfig):
    name = 'monitoring'

    def ready(self):
        from monitoring import signals # noqa
