from django.apps import AppConfig


class TestPassingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_passing'
