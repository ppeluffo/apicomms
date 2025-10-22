#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
"""
import redis
from config import settings
from flask import current_app

class ApiBdRedis:

    def __init__(self, logger):
        self.logger = logger
        self.rh = redis.Redis( settings.BDREDIS_HOST, settings.BDREDIS_PORT,settings.BDREDIS_DB, socket_connect_timeout=1)
        
    def ping(self):
        """
        Si el server responde, el ping da True.
        Si no responde, sale por exception.
        """
        #self.logger.info("TESTING LOGGER INFO")
        #self.logger.debug("TESTING LOGGER DEBUG")
        #self.logger.error("TESTING LOGGER ERROR")

        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            self.rh.ping()
            ds_rsp = {'status_code': 200,
                      'version':settings.API_VERSION,
                      'REDIS_HOST':settings.BDREDIS_HOST,
                      'REDIS_PORT': settings.BDREDIS_PORT }
        
        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            ds_rsp = {'status_code': 502,  'msg':f"{e}" }
            
        return ds_rsp
    
    ############################################################

    def save_dataline(self, unit=None, pk_dataline=None):
        """
        """
        self.logger.debug("")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            _ = self.rh.hset( unit, 'PKLINE', pk_dataline )
            d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        #
        return d_rsp
    
    def save_timestamp(self, unit=None, pk_timestamp=None):
        """
        Los timestamps se ponen en un hash, con clave la unit, y picleados
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            _ = self.rh.hset( 'TIMESTAMP', unit, pk_timestamp )
            d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        # 
        return d_rsp
    
    def enqueue_dataline(self, unit=None, pk_datastruct=None):

        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            _ = self.rh.rpush( 'RXDATA_QUEUE', pk_datastruct)
            d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        # 
        return d_rsp

    ############################################################
 
    def read_configuracion_unidad(self, unit_id=None):
        """
        La BD redis envia un string (datos pickleados)
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            pkconfig = self.rh.hget( unit_id, 'PKCONFIG')
            if pkconfig is None:
                d_rsp = {'status_code': 404 }
            else:
                d_rsp = {'status_code': 200, 'pkconfig':pkconfig}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        #self.logger.debug(f"unit_id={unit_id}, d_rsp={d_rsp}")   
        return d_rsp
    
    def set_configuracion_unidad(self, unit_id=None, pkconfig=None):
        """
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            _ = self.rh.hset( unit_id,'PKCONFIG', pkconfig)
            d_rsp = {'status_code': 200}
        
        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp

    ############################################################

    def read_ordenesplc(self, unit=None):
        """
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            pk_ordenes_plc = self.rh.hget( unit, 'PKATVISE' )
            if pk_ordenes_plc is None:
                d_rsp = {'status_code': 404 }
            else:
                d_rsp = {'status_code': 200, 'pk_ordenes_plc':pk_ordenes_plc}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp
    
    def delete_ordenesplc(self, unit=None):
        """
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            _ = self.rh.hdel(unit, 'PKATVISE' )
            d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        #
        return d_rsp

    def read_dataline(self, unit=None):
        """
        Lee el campo PKLINE del HSET de la unidad
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            pk_dataline = self.rh.hget( unit, 'PKLINE')
            if pk_dataline is None:
                d_rsp = {'status_code': 404 }
            else:
                d_rsp = {'status_code': 200, 'pk_dataline':pk_dataline }

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        #
        return d_rsp
    
    ############################################################

    def set_id_and_uid(self, uid=None, id=None):
        
        """
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            _ = self.rh.hset( 'RECOVERIDS', uid,id )
            d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        
        return d_rsp

    def get_id_from_uid(self, uid=None):

        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            id = self.rh.hget('RECOVERIDS', uid )
            if id is None:
                d_rsp = {'status_code': 404 }
            else:
                d_rsp = {'status_code': 200, 'id':id }

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        #
        return d_rsp

    ############################################################
   
    def read_ordenes(self, unit=None):
        """
        Devuelve un string pickeado
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            pk_ordenes = self.rh.hget( unit, 'PKORDENES' )
            if pk_ordenes is None:
                d_rsp = {'status_code': 404 }
            else:
                d_rsp = {'status_code': 200, 'pk_ordenes':pk_ordenes}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp

    def delete_ordenes(self, unit=None):
        """
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            _ = self.rh.hdel(unit, 'PKORDENES' )
            d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        #
        return d_rsp

    ############################################################

    def delete_configuracion_unidad(self, unit_id=None):
        """
        """
        self.logger.debug(f"")
        current_app.config["ACCESOS_REDIS"] += 1

        try:
            _ = self.rh.hdel(unit_id, 'PKCONFIG')
            d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        #
        return d_rsp

