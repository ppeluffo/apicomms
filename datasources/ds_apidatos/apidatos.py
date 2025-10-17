#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
"""

from config import settings
import requests

class Apidatos:

    def __init__(self, logger):
        self.logger = logger
        self.BASE_URL = settings.API_DATOS_URLBASE

    def ping(self):
        """
        Si el server responde, el ping da True.
        Si no responde, sale por exception.
        """
        self.logger.debug(f"")

        try:
            r = requests.get(f"{self.BASE_URL}/ping", timeout=10 )
            d_rsp = {'status_code': r.status_code, 'json': r.json() }

        except Exception as e: 
            self.logger.error( f"Error-> {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp

    def read_configuration(self, id=None):
        """
        Le pedimos a la apiredis los datos de configuracion del equipo con id.
        """
        self.logger.debug("")
        
        try:
            params = {'unit': id }
            r = requests.get(f"{self.BASE_URL}/config", params=params, timeout=10 )
            
        except Exception as e: 
            self.logger.error( f"Error-> {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        
        if r.status_code == 200:
            # Cada elemento es del tipo: {'TYPE':args['type'], 'ID':args['unit'], 'D_LINE':d_params}.
            payload = r.json()
            l_datastruct = payload.get('l_datastruct',[])
            d_rsp = {'status_code': 200,  'l_datastruct':l_datastruct }
        else:
            d_rsp = {'status_code': r.status_code }

        self.logger.debug(f"d_rsp={d_rsp}")
        return d_rsp         
