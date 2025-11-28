from django.apps import AppConfig


class MembersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'members_app'

    def ready(self):
        import members_app.signals
