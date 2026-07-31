from django.apps import AppConfig
import threading, logging
logger = logging.getLogger(__name__)

class RoutingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'routing'

    def ready(self):
        import sys
        if 'runserver' not in sys.argv and 'gunicorn' not in sys.argv[0]:
            return
        def _load():
            try:
                from django.conf import settings
                from .graph_manager import GraphManager
                gm = GraphManager.get_instance()
                gm.load_districts(
                    districts=list(settings.GRAPH_DISTRICTS),
                    cache_dir=str(settings.GRAPH_CACHE_DIR)
                )
            except Exception as e:
                logger.error(f'Graph load error: {e}')
        threading.Thread(target=_load, daemon=True).start()
