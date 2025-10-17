#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import logging
import sys
import os
from config import settings

def configure_logger(name: str = "app", gunicorn: bool = False) -> logging.Logger:
    
    logger = logging.getLogger(name)
    
    # Leer nivel de logs desde variable de entorno (default: INFO)
    #logger.setLevel(logging.INFO)
    #log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = settings.LOG_LEVEL.upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Si la app corre bajo gunicorn → reutilizamos sus handlers
    if gunicorn:
        gunicorn_logger = logging.getLogger("gunicorn.error")
        logger.handlers = gunicorn_logger.handlers
        logger.setLevel(gunicorn_logger.level)
    else:
        # Configuración estándar cuando corre standalone
        # Sólo añadir handler si no hay
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - [%(module)s.%(funcName)s] - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    return logger
