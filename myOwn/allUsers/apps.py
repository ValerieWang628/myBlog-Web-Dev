from django.apps import AppConfig


class AllusersConfig(AppConfig):
    name = 'allUsers'

    def ready(self):
        import allUsers.signals
