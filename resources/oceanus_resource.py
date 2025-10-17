#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse, request
from dependency_injector.wiring import inject, Provide
from container import Container
import datetime as dt
from servicios.oceanus_service import OceanusService


class OceanusResource(Resource):

    @inject
    def __init__(self, service: OceanusService = Provide[Container.oceanus_service], logger = Provide[Container.logger]):
        self.oceanus_service = service
        self.logger = logger
            
    def post(self):
        '''
        Procesa los POST que vienen de las estaciones OCEANUS
        Del URL leo los parámetro ID,VER,TYPE
        Los datos vienen en el cuerpo del POST.
        '''
        self.logger.debug("")
        
        parser = reqparse.RequestParser()
        parser.add_argument('ID',type=str,location='args',required=True)
        parser.add_argument('VER',type=str,location='args',required=True)
        parser.add_argument('TYPE',type=str,location='args',required=True)
        args=parser.parse_args()
        id = args['ID']
        version = args['VER']
        tipo = args['TYPE']
        payload = request.get_data()

        _ = self.oceanus_service.procesar_frame(id=id, payload=payload)

        # Las estaciones OCEANUS solo envian datos POST. No procesan respuestas
        return {}, 200

    


