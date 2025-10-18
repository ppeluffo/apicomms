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

        except Exception as e: 
            self.logger.error( f"Error-> {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        
        if r.status_code == 200:
            payload = r.json()
            d_rsp = {'status_code':200} | payload
        else:
            d_rsp = {'status_code': r.status_code }
        
        #self.logger.debug(f"d_rsp={d_rsp}")
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
            payload = r.json()
            d_rsp = {'status_code':200} | payload
        else:
            d_rsp = {'status_code': r.status_code }
        
        #self.logger.debug(f"d_rsp={d_rsp}")
        return d_rsp        

    def get_uid2id(self, uid=None):
        """
        """
        self.logger.debug("")

        try:
            params = {'uid': uid }
            r = requests.get(f"{self.BASE_URL}/uid2id", params=params, timeout=10 )
            
        except Exception as e: 
            self.logger.error( f"Error-> {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        
        if r.status_code == 200:
            payload = r.json()
            d_rsp = {'status_code':200} | payload
        else:
            d_rsp = {'status_code': r.status_code }

        #self.logger.debug(f"d_rsp={d_rsp}")
        return d_rsp
    
    def set_uid2id(self, uid=None, id=None):
        """
        """
        self.logger.debug("")
        
        try:
            jparams = {'uid': uid, 'id': id }
            r = requests.put(f"{self.BASE_URL}/uid2id", json=jparams, timeout=10 )
            d_rsp = {'status_code': 200 }

        except Exception as e: 
            self.logger.error( f"Error-> {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp