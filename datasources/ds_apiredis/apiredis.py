#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
"""
from flask import current_app
from config import settings
import requests

class Apiredis:

    def __init__(self, logger):
        self.logger = logger
        self.BASE_URL = settings.API_REDIS_URLBASE

    def read_dataline(self, unit=None):
        """
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        params = {'unit':unit}
        try:
            r = requests.get(f"{self.BASE_URL}/dataline", params=params, timeout=10 )
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
            
    def put_dataline(self, id=None, tipo=None, jparams=None):
        """
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        params = {'unit':id, 'type':tipo}
        #self.logger.debug(f"params={params}")
        #self.logger.debug(f"jparams={jparams}")
        try:
            r = requests.put(f"{self.BASE_URL}/dataline", params=params, json=jparams, timeout=10 )

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
      
    def ping(self):
        """
        Si el server responde, el ping da True.
        Si no responde, sale por exception.
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

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
        current_app.config["ACCESOS_REDIS"] += 1
        
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

    def set_configuration(self, id=None, d_config=None):
        """
        """
        self.logger.debug("")
        current_app.config["ACCESOS_REDIS"] += 1

        jparams = d_config
        try:
            params = {'unit': id }
            r = requests.put(f"{self.BASE_URL}/config", json=jparams, timeout=10 )
            
        except Exception as e: 
            self.logger.error( f"Error-> {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        d_rsp = {'status_code': r.status_code }

        self.logger.debug(f"d_rsp={d_rsp}")
        return d_rsp

    def read_ordenesplc(self, unit=None):
        """
        """
        self.logger.debug("")
        current_app.config["ACCESOS_REDIS"] += 1
        
        try:
            params = {'unit': unit }
            r = requests.get(f"{self.BASE_URL}/ordenesplc", params=params, timeout=10 )
            
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
    
    def delete_ordenesplc(self, unit=None):
        """
        """
        self.logger.debug("")
        current_app.config["ACCESOS_REDIS"] += 1
        
        try:
            params = {'unit': unit }
            r = requests.delete(f"{self.BASE_URL}/ordenesplc", params=params, timeout=10 )
            d_rsp = {'status_code': 200 }
            
        except Exception as e: 
            self.logger.error( f"Error-> {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        
        return d_rsp   
    
    def get_uid2id(self, uid=None):
        """
        """
        self.logger.debug("")
        current_app.config["ACCESOS_REDIS"] += 1
        
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
        current_app.config["ACCESOS_REDIS"] += 1
        
        try:
            jparams = {'uid': uid, 'id': id }
            r = requests.put(f"{self.BASE_URL}/uid2id", json=jparams, timeout=10 )
            d_rsp = {'status_code': 200 }

        except Exception as e: 
            self.logger.error( f"Error-> {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp