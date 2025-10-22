#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
"""

from .models import Usuarios, Configuraciones, Online, RecoverId, Historica
from sqlalchemy import text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import insert

from datetime import datetime, timedelta

from config import settings

class ApiBdPgsql:

    def __init__(self, session_factory, logger):
        self.session_factory = session_factory
        self.logger = logger

    def ping(self):
        """
        Si el server responde, el ping da True.
        Si no responde, sale por exception.
        """
        self.logger.debug(f"")

        try:
            with self.session_factory() as session:
                session.execute(text("SELECT 1"))
                d_rsp = {'status_code': 200,
                         'version': settings.API_VERSION,
                         "SQL_HOST": settings.PGSQL_HOST,
                         "SQL_PORT": settings.PGSQL_PORT }
        except Exception as e:
            self.logger.error(f"PgSQL Error: {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp
    
    ############################################################

    def read_configuracion_unidad(self, unit_id=None):
        """
        Retorna la configuracion de la unidad tal cual se lee.
        Retorna el campo jconfig de la base de datos.
        JCONFIG_RAW=(
            {'version': '1.1.0', 
             'BASE': {'ALMLEVEL': '10', 'SAMPLES': '1', 'PWRS_HHMM1': '1530', 'PWRS_HHMM2': '1550', 'PWRS_MODO': '1', 'TDIAL': '900', 'TPOLL': ..
             . (1784 characters truncated) ... LOT10': {'PRES': 0.0, 'TIME': '0000'}, 'SLOT11': {'PRES': 0.0, 'TIME': '0000'}}, 
             'CONSIGNA': {'ENABLE': 'FALSE', 'DIURNA': '730', 'NOCTURNA': '2300'}
             },)
        La respuesta es una tupla por lo tanto el valor real es t[0]

        SIEMPRE EL DATASOURCE DEVUELVE LO QUE OBTIENE DE LA BASE DE DATOS !!.
        LO MODIFICA EL SERVICIO !!.
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                jconfig_raw = session.query(Configuraciones.jconfig).filter(Configuraciones.unit_id == unit_id).first()
                if jconfig_raw is None:
                    status_code = 204
                else:
                    status_code = 200
                d_rsp = {'status_code': status_code, 'jconfig_raw': jconfig_raw }

        except Exception as e:
            self.logger.error(f"{e}")
            d_rsp = { 'status_code': 400, 'msg': e}

        #self.logger.debug(f"d_rsp={d_rsp}") 
        return d_rsp
    
    ############################################################

    def set_id_and_uid(self, id=None, uid=None):
        """
        Guarda (actualiza) un registro uid-id de la tabla recoverid
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                new_rcd = RecoverId(uid=uid, id=id)
                _ = session.add(new_rcd)
                session.commit()
                d_rsp = {'status_code': 200, 'uid':uid, 'id':id}

        except Exception as e:
            self.logger.error(f"PgSQL {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp      

    def get_id_from_uid(self, uid=None):
        """
        Retorna la configuracion de la unidad 
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                recoverid_rcd = session.query(RecoverId).filter(RecoverId.uid == uid).first()
                if recoverid_rcd is None:
                    d_rsp = {'status_code': 204, 'recoverid_rcd': recoverid_rcd }
                else:    
                    d_rsp = {'status_code': 200, 'recoverid_rcd': recoverid_rcd }

        except Exception as e:
            self.logger.error(f"PgSQL {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp        

    ############################################################

