#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource
from dependency_injector.wiring import inject, Provide
from container import Container
import datetime as dt

class TestResource(Resource):

    @inject
    def __init__(self, logger = Provide[Container.logger]):
        self.logger = logger
        
    def get(self):

        # Solicito el servicio correspondiente.
        self.logger.debug("")
            
        now=dt.datetime.now().strftime('%y%m%d%H%M%S')
        response = f'<html>CLASS=DATA&CLOCK={now};</html>'
        return response, 200

    


