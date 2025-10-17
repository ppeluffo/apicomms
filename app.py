#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
API REST para acceder a los servicios de REDIS del servidor de comunicaciones

"""

import logging
from config import settings

from resources import ping_resource
from resources import test_resource
from resources import oceanus_resource
from resources import plc_resource

from container import Container

from flask import Flask
from flask_restful import Api

from utilidades.login_config import configure_logger

def create_app(gunicorn: bool = False):

    app = Flask(__name__)
    api = Api(app)

    container = Container()

    app.config["ACCESOS_REDIS"] = 0

    # Sobrescribir logger según modo
    container.logger.override(configure_logger("api-comms", gunicorn=gunicorn))

    container.init_resources()
    container.wire(modules=[__name__])

    api.add_resource( ping_resource.PingResource, '/apicomms/ping')
    api.add_resource( test_resource.TestResource, '/apicomms/test')
    api.add_resource( oceanus_resource.OceanusResource, '/apioceanus')
    api.add_resource( plc_resource.PlcResource, '/apiplc')
   
    return app

# Lineas para cuando corre en gurnicorn
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app = create_app(gunicorn=True)
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info(f'Starting APICOMMS')


# Lineas para cuando corre en modo independiente
if __name__ == '__main__':
    app = create_app(gunicorn=False)
    app.run(host='0.0.0.0', port=5000, debug=True)

