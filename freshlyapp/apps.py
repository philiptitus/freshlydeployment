from django.apps import AppConfig


class FreshlyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'freshlyapp'



    def ready(self):
        import freshlyapp.signals  # Import the signals module to connect the signal handlers
