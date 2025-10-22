#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask import make_response
from flask_restful import Resource, reqparse, request
from dependency_injector.wiring import inject, Provide
from container import Container
from servicios.plc_service import PlcService
import time
from flask import current_app

class PlcResource(Resource):

    @inject
    def __init__(self, service: PlcService = Provide[Container.plc_service], logger = Provide[Container.logger]):
        self.plc_service = service
        self.logger = logger
            
    def post(self):
        '''
        Procesa los POST que vienen de las estaciones OCEANUS
        Del URL leo los parámetro ID,VER,TYPE
        Los datos vienen en el cuerpo del POST.

        IMPORTANTE:
        - los datos binarios no se pueden enviar crudos dentro de un JSON (no son texto válido UTF-8).
        - Flask envía el bytestream directamente como cuerpo binario, no JSON
        - Esto  es válido, porque HTTP no prohíbe enviar datos binarios.
            * No estás usando json=... en el requests.post().
            * La API no está retornando JSON, sino un flujo binario.
            * El header Content-Type debería ser algo como "application/octet-stream"
        '''

        start = time.time()
        current_app.config["ACCESOS_REDIS"] = 0

        self.logger.debug("")
        
        parser = reqparse.RequestParser()
        parser.add_argument('ID',type=str,location='args',required=True)
        parser.add_argument('VER',type=str,location='args',required=True)
        parser.add_argument('TYPE',type=str,location='args',required=True)
        args=parser.parse_args()

        unit_id = args['ID']
        version = args['VER']
        tipo = args['TYPE']
        payload = request.get_data()

        self.logger.debug(f"payload={payload}")

        d_rsp = self.plc_service.procesar_frame(unit_id=unit_id, payload=payload)
        assert isinstance(d_rsp, dict)
        status_code = d_rsp.get('status_code',0)
        if status_code == 200:
            # La funcion make_response es de FLASK !!!
            # sresp es un string binario que representa el mapa de memoria, que
            # se manda al PLC.    
            bytestream = d_rsp.get('bytestream',None)
        else:
            bytestream = b''
            
        self.logger.debug(f"bytestream={bytestream}")

        response = make_response(bytestream)
        response.headers['Content-type'] = 'application/binary'
         
        # Stats
        end = time.time()
        elapsed_time = (end - start) * 1000
        self.logger.info(f"POST: transaction time: {elapsed_time:.2f} msecs, Accesos REDIS: {current_app.config['ACCESOS_REDIS']}")

        return response
    


    


