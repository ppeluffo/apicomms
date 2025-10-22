#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from utilidades.str2int import str2int
from utilidades.uhash import u_hash

class DlgAinputFrameUsecase:
    """
    """

    def __init__(self, repo, logger):
        self.repo = repo
        self.logger = logger
        self.dlgid = None
    
    def get_ainputs_hash_from_config(self, d_conf=None):
        '''
        Calculo el hash para la todas las versiones
        '''
        self.logger.debug("")

        xhash = 0
        for channel in ['A0','A1','A2']:
            enable = d_conf.get('AINPUTS',{}).get(channel,{}).get('ENABLE','FALSE')
            name = d_conf.get('AINPUTS',{}).get(channel,{}).get('NAME','X')
            imin = str2int( d_conf.get('AINPUTS',{}).get(channel,{}).get('IMIN','0'))
            imax = str2int( d_conf.get('AINPUTS',{}).get(channel,{}).get('IMAX','0'))
            mmin = float( d_conf.get('AINPUTS',{}).get(channel,{}).get('MMIN','0'))
            mmax = float( d_conf.get('AINPUTS',{}).get(channel,{}).get('MMAX','0'))
            offset = float( d_conf.get('AINPUTS',{}).get(channel,{}).get('OFFSET','0'))
            hash_str = f'[{channel}:{enable},{name},{imin},{imax},{mmin:.02f},{mmax:.02f},{offset:.02f}]'
            xhash = u_hash(xhash, hash_str)
            #self.logger.debug(f'hash_str={hash_str}, xhash={xhash}')
        return xhash
    
    def get_response_ainputs(self, d_conf=None):
        '''
        Armo la respuesta para todas las versiones
        '''
        self.logger.debug("")
        
        response = 'CLASS=CONF_AINPUTS&'
        for channel in ['A0','A1','A2']:
            enable = d_conf.get('AINPUTS',{}).get(channel,{}).get('ENABLE', 'FALSE')
            name = d_conf.get('AINPUTS',{}).get(channel,{}).get('NAME', 'X')
            imin = str2int(d_conf.get('AINPUTS',{}).get(channel,{}).get('IMIN', '4'))
            imax = str2int(d_conf.get('AINPUTS',{}).get(channel,{}).get('IMAX', '20'))
            mmin = float(d_conf.get('AINPUTS',{}).get(channel,{}).get('MMIN', 0.00))
            mmax = float(d_conf.get('AINPUTS',{}).get(channel,{}).get('MMAX', 10.00))
            offset = float(d_conf.get('AINPUTS',{}).get(channel,{}).get('OFFSET', 0.00))
            response += f'{channel}={enable},{name},{imin},{imax},{mmin},{mmax},{offset}&'
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
        self.logger.debug(f"id={self.dlgid}, d_rsp={d_rsp}")
        
        if d_rsp.get('status_code',0) != 200:
            self.logger.error(f"CONFIG ERROR")
            d_rsp = { 'status_code': 200, 'raw_response': 'CLASS=CONF_BASE&CONFIG=ERROR' }
            return d_rsp
 
        d_conf = d_rsp['d_config']
        if 'ANALOGS' not in d_conf.keys():
            self.logger.error(f"NO ANALOGS in keys !!. Default config.")
            d_rsp = { 'status_code': 200, 'raw_response': 'CLASS=ERROR' }
            return d_rsp
        
        # 2) Calculo el hash de la configuracion de la BD.
        bd_hash = self.get_ainputs_hash_from_config(d_conf)
        fx_hash = int(d_params.get('HASH',0), 16)
        self.logger.debug(f"ID={self.dlgid}: BD_hash={bd_hash}, UI_hash={fx_hash}")

        if bd_hash == fx_hash:
            raw_response = 'CLASS=CONF_AINPUTS&CONFIG=OK'
            d_rsp = { 'status_code': 200, 'raw_response': raw_response }
            self.logger.debug(f"ID={self.dlgid},RSP=[{raw_response}]")
            return d_rsp
            
        # 3) No coinciden: mando la nueva configuracion
        raw_response = self.get_response_ainputs(d_conf)
        d_rsp = { 'status_code': 200, 'raw_response': raw_response }
        self.logger.debug(f"ID={self.dlgid},RSP=[{raw_response}]")
        return d_rsp


