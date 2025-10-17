#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource
from dependency_injector.wiring import inject, Provide
from container import Container
from servicios.ping_service import PingService

class PingResource(Resource):

    @inject
    def __init__(self, service: PingService = Provide[Container.ping_service], logger = Provide[Container.logger]):
        self.ping_service = service
        self.logger = logger
        
    def get(self):

        # Solicito el servicio correspondiente.
        self.logger.debug("")
            
        d_rsp = self.ping_service.ping()
        status_code = d_rsp.pop('status_code', 500)

        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 502:
            _ = d_rsp.pop('msg', '')
            d_rsp['msg'] = "SERVICIO NO DISPONIBLE TEMPORALMENTE"
        
        return d_rsp, status_code
    


