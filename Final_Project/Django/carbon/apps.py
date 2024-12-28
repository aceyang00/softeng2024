from django.apps import AppConfig


class CarbonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "carbon"
from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app_name'

    def ready(self):
        # signals.py 파일을 가져옵니다.
        import your_app_name.signals
