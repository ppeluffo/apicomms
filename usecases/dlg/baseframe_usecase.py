#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from utilidades.str2int import str2int
from utilidades.uhash import u_hash

class DlgBaseFrameUsecase:
    """
    """

    def __init__(self, repo, logger):
        self.repo = repo
        self.logger = logger
        self.dlgid = None
    
    def get_base_hash_from_config(self, d_conf=None):
        '''
        Calculo el hash para la todas las versiones
        '''
        self.logger.debug("V0")

        xhash = 0
        timerpoll = str2int(d_conf.get('BASE',{}).get('TPOLL','0'))
        timerdial = str2int(d_conf.get('BASE',{}).get('TDIAL','0'))
        pwr_modo = str2int(d_conf.get('BASE',{}).get('PWRS_MODO','0'))
        pwr_hhmm_on = str2int(d_conf.get('BASE',{}).get('PWRS_HHMM1','601'))
        pwr_hhmm_off = str2int(d_conf.get('BASE',{}).get('PWRS_HHMM2','2201'))
        #
        hash_str = f'[TIMERPOLL:{timerpoll:03d}]'
        xhash = u_hash(xhash, hash_str)
        #self.logger.debug(f'hash_str={hash_str}, xhash={xhash}')
        #
        hash_str = f'[TIMERDIAL:{timerdial:03d}]'
        xhash = u_hash(xhash, hash_str)
        #self.logger.debug(f'hash_str={hash_str}, xhash={xhash}')
        #
        hash_str = f'[PWRMODO:{pwr_modo}]'
        xhash = u_hash(xhash, hash_str)
        #self.logger.debug(f'hash_str={hash_str}, xhash={xhash}')
        #
        hash_str = f'[PWRON:{pwr_hhmm_on:04}]'
        xhash = u_hash(xhash, hash_str)
        #self.logger.debug(f'hash_str={hash_str}, xhash={xhash}')
        #
        hash_str = f'[PWROFF:{pwr_hhmm_off:04}]'
        xhash = u_hash(xhash, hash_str)
        #self.logger.debug(f'hash_str={hash_str}, xhash={xhash}')
        #
        samples = str2int(d_conf.get('BASE',{}).get('SAMPLES','1'))
        almlevel = str2int(d_conf.get('BASE',{}).get('ALMLEVEL','0'))
        hash_str = f'[SAMPLES:{samples:02}]'
        xhash = u_hash(xhash, hash_str)
        #self.logger.debug(f'hash_str={hash_str}, xhash={xhash}')
        #
        hash_str = f'[ALMLEVEL:{almlevel:02}]'
        xhash = u_hash(xhash, hash_str)
        #self.logger.debug(f'hash_str={hash_str}, xhash={xhash}')
        return xhash
    
    def get_response_base(self, d_conf=None):
        '''
        Armo la respuesta para todas las versiones
        '''
        self.logger.debug("V0")

        timerpoll = str2int( d_conf.get('BASE',{}).get('TPOLL','0'))
        #self.logger.debug(f'timerpoll={timerpoll}')
        timerdial = str2int(d_conf.get('BASE',{}).get('TDIAL','0'))
        #self.logger.debug(f'timerdial={timerdial}')
        pwr_modo = str2int(d_conf.get('BASE',{}).get('PWRS_MODO','0'))
        pwr_hhmm_on = str2int(d_conf.get('BASE',{}).get('PWRS_HHMM1','600'))
        pwr_hhmm_off = str2int(d_conf.get('BASE',{}).get('PWRS_HHMM2','2200'))
        if pwr_modo == 0:
            s_pwrmodo = 'CONTINUO'
        elif pwr_modo == 1:
            s_pwrmodo = 'DISCRETO'
        else:
            s_pwrmodo = 'MIXTO'
        #
        samples = str2int( d_conf.get('BASE',{}).get('SAMPLES','1'))
        almlevel = str2int( d_conf.get('BASE',{}).get('ALMLEVEL','0'))
        #
        response = 'CLASS=CONF_BASE&'
        response += f'TPOLL={timerpoll}&TDIAL={timerdial}&PWRMODO={s_pwrmodo}&PWRON={pwr_hhmm_on:04}&PWROFF={pwr_hhmm_off:04}'
        response += f'&SAMPLES={samples}&ALMLEVEL={almlevel}'
        #self.logger.debug(f'response={response}')
        return response
    
    def procesar_frame(self, d_params=None):
        """
        ID=PABLO&TYPE=SPXR3&VER=1.0.0&CLASS=CONF_BASE&UID=42125128300065090117010400000000&HASH=0x11
        ID=SPQTEST&TYPE=SPQ_AVRDA&VER=1.2.3&CLASS=CONF_BASE&UID=42138365900098090136013700000000&IMEI=868191051391785&ICCID=8959801023149326185F&CSQ=51&HASH=0x42
        """
        self.logger.debug("")
 
        self.dlgid = d_params.get('ID',None)
        if self.dlgid is None:
            self.logger.info(f"ERROR dlgid None")
            return {'status_code':400}

        # 1) Le pido al repositorio que me de la configuracion
        d_rsp = self.repo.leer_configuracion_unidad(self.dlgid)
        assert isinstance(d_rsp, dict)
        self.logger.debug(f"id={self.dlgid}, d_rsp={d_rsp}")
        
        if d_rsp.get('status_code',0) != 200:
            self.logger.error(f"CONFIG ERROR")
            d_rsp = { 'status_code': 200, 'raw_response': 'CLASS=CONF_BASE&CONFIG=ERROR' }
            return d_rsp
 
        d_conf = d_rsp['d_config']
        if 'BASE' not in d_conf.keys():
            self.logger.error(f"NO BASE in keys !!. Default config.")
            d_rsp = { 'status_code': 200, 'raw_response': 'CLASS=ERROR' }
            return d_rsp
        
        # 2) Actualizo uid2id
        uid = d_params.get('UID',None)
        _ = self.repo.update_uid2id( self.dlgid, uid)

        # 3) Actualizo los parámetros de comunicaciones
        _ = self.repo.update_commsparameters(d_params)

        # 4) Calculo el hash de la configuracion de la BD.
        bd_hash = self.get_base_hash_from_config(d_conf)
        fx_hash = int(d_params.get('HASH',0), 16)
        self.logger.debug(f"ID={self.dlgid}: BD_hash={bd_hash}, UI_hash={fx_hash}")

        if bd_hash == fx_hash:
            raw_response = 'CLASS=CONF_BASE&CONFIG=OK'
            d_rsp = { 'status_code': 200, 'raw_response': raw_response }
            self.logger.debug(f"ID={self.dlgid},RSP=[{raw_response}]")
            return d_rsp
            
        # 5) No coinciden: mando la nueva configuracion
        raw_response = self.get_response_base(d_conf)
        d_rsp = { 'status_code': 200, 'raw_response': raw_response }
        self.logger.debug(f"ID={self.dlgid},RSP=[{raw_response}]")
        return d_rsp

