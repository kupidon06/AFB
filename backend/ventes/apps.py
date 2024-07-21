from django.apps import AppConfig

class VentesConfig(AppConfig):
    name = 'ventes'

    def ready(self):
        # Importer les signaux
        import ventes.signals
