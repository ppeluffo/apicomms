#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask import make_response
from flask_restful import Resource, reqparse, request
from dependency_injector.wiring import inject, Provide
from container import Container
from servicios.dlg_service import DlgService
import time
from flask import current_app

class DlgResource(Resource):

    @inject
    def __init__(self, service: DlgService = Provide[Container.dlg_service], logger = Provide[Container.logger]):
        self.dlg_service = service
        self.logger = logger
            
    def get(self):
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

        # Parseo todos las variables de querystring
        d_params = request.args.to_dict()                   
        self.logger.debug(f"d_params={d_params}")

        d_rsp = self.dlg_service.procesar_frame(d_params)
        
        assert isinstance(d_rsp, dict)
        status_code = d_rsp.get('status_code',0)
        if status_code == 200: 
            raw_response = d_rsp.get('raw_response', "")
        else:
            raw_response = ""
            
        self.logger.debug(f"raw_response->{raw_response}")
        response = (f'<html>{raw_response}</html>')
        
        # Stats
        end = time.time()
        elapsed_time = (end - start) * 1000
        self.logger.info(f"GET: transaction time: {elapsed_time:.2f} msecs, Accesos REDIS: {current_app.config['ACCESOS_REDIS']}")

        return response, status_code
    

    


