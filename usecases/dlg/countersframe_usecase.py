#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from utilidades.str2int import str2int
from utilidades.uhash import u_hash
from flask import current_app
from utilidades.selective_logger import slogger

class DlgCountersFrameUsecase:
    """
    """

    def __init__(self, repo, logger):
        self.repo = repo
        self.logger = logger
        self.dlgid = None
    
    def get_counters_hash_from_config(self, d_conf=None):
        '''
        Calculo el hash para la todas las versiones
        '''
        self.logger.debug("")

        xhash = 0
        for channel in ['C0']:
            enable = d_conf.get('COUNTERS',{}).get(channel,{}).get('ENABLE','FALSE')
            name = d_conf.get('COUNTERS',{}).get(channel,{}).get('NAME','X')
            modo = d_conf.get('COUNTERS',{}).get(channel,{}).get('MODO','CAUDAL')
            magpp = float(d_conf.get('COUNTERS',{}).get(channel,{}).get('MAGPP','0'))
            hash_str = f'[{channel}:{enable},{name},{magpp:.03f},{modo}]'
            xhash = u_hash(xhash, hash_str)
            #self.logger.debug(f'hash_str={hash_str}')

        return xhash
    
    def get_response_counters(self, d_conf=None):
        '''
        Armo la respuesta para todas las versiones
        '''
        self.logger.debug("")
        
        response = 'CLASS=CONF_COUNTERS&'
        for channel in ['C0']:
            enable = d_conf.get('COUNTERS',{}).get(channel,{}).get('ENABLE','FALSE')
            name = d_conf.get('COUNTERS',{}).get(channel,{}).get('NAME', 'X')
            magpp = float(d_conf.get('COUNTERS',{}).get(channel,{}).get('MAGPP', 1.00))
            str_modo = d_conf.get('COUNTERS',{}).get(channel,{}).get('MODO','CAUDAL')
            response += f'{channel}={enable},{name},{magpp},{str_modo}&'
        #
        response = response[:-1]
        return response
        
    def procesar_frame(self, d_params=None):
        """
        """
        self.logger.debug("")
 
        self.dlgid = d_params.get('ID',None)
        if self.dlgid is None:
            self.logger.info(f"ERROR dlgid None")
            return {'status_code':400}

        # 1) Le pido al repositorio que me de la configuracion
        d_rsp = self.repo.leer_configuracion_unidad(self.dlgid)
        assert isinstance(d_rsp, dict)
        slogger(f"d_rsp={d_rsp}")
        
        if d_rsp.get('status_code',0) != 200:
            self.logger.error(f"CONFIG ERROR")
            d_rsp = { 'status_code': 200, 'raw_response': 'CLASS=CONF_BASE&CONFIG=ERROR' }
            return d_rsp
 
        d_conf = d_rsp['d_config']
        if 'COUNTERS' not in d_conf.keys():
            self.logger.error(f"NO COUNTERS in keys !!. Default config.")
            d_rsp = { 'status_code': 200, 'raw_response': 'CLASS=ERROR' }
            return d_rsp
        
        # 2) Calculo el hash de la configuracion de la BD.
        bd_hash = self.get_counters_hash_from_config(d_conf)
        fx_hash = int(d_params.get('HASH',0), 16)
        slogger(f"BD_hash={bd_hash}, UI_hash={fx_hash}")

        if bd_hash == fx_hash:
            raw_response = 'CLASS=CONF_COUNTERS&CONFIG=OK'
            d_rsp = { 'status_code': 200, 'raw_response': raw_response }
            return d_rsp
            
        # 3) No coinciden: mando la nueva configuracion
        raw_response = self.get_response_counters(d_conf)
        d_rsp = { 'status_code': 200, 'raw_response': raw_response }
        return d_rsp

