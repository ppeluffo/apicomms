#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from utilidades.str2int import str2int
from utilidades.uhash import u_hash

class DlgModbusFrameUsecase:
    """
    """

    def __init__(self, repo, logger):
        self.repo = repo
        self.logger = logger
        self.dlgid = None
    
    def get_modbus_hash_from_config(self, d_conf=None):
        '''
        Calculo el hash para la todas las versiones
        '''
        self.logger.debug("")

        xhash = 0
        enable = d_conf.get('MODBUS',{}).get('ENABLE','FALSE')
        localaddr = str2int(d_conf.get('MODBUS',{}).get('LOCALADDR','1'))
        hash_str = f'[{enable},{localaddr:02d}]'
        xhash = u_hash(xhash, hash_str)
        #self.logger.debug(f'hash_str={hash_str}{xhash}')
        #,
        for channel in ['M0','M1','M2','M3','M4']:
            enable = d_conf.get('MODBUS',{}).get(channel,{}).get('ENABLE','FALSE')
            name = d_conf.get('MODBUS',{}).get(channel,{}).get('NAME','X')
            sla_addr = str2int(d_conf.get('MODBUS',{}).get(channel,{}).get('SLA_ADDR','0'))
            reg_addr = str2int(d_conf.get('MODBUS',{}).get(channel,{}).get('ADDR','0'))
            nro_regs = str2int(d_conf.get('MODBUS',{}).get(channel,{}).get('NRO_RECS','0'))
            fcode = str2int(d_conf.get('MODBUS',{}).get(channel,{}).get('FCODE','0'))
            mtype = d_conf.get('MODBUS',{}).get(channel,{}).get('TYPE','U16')
            codec = d_conf.get('MODBUS',{}).get(channel,{}).get('CODEC','C0123')
            pow10 = str2int(d_conf.get('MODBUS',{}).get(channel,{}).get('POW10','0'))
            hash_str = f'[{channel}:{enable},{name},{sla_addr:02d},{reg_addr:04d},{nro_regs:02d},{fcode:02d},{mtype},{codec},{pow10:02d}]'
            xhash = u_hash(xhash, hash_str)
            #self.logger.debug(f'hash_str={hash_str}{xhash}')
        #
        return xhash
    
    def get_response_modbus(self, d_conf=None):
        '''
        Armo la respuesta para todas las versiones
        '''
        self.logger.debug("")
        
        enable = d_conf.get('MODBUS',{}).get('ENABLE','FALSE')
        localaddr = str2int(d_conf.get('MODBUS',{}).get('LOCALADDR','0x01'))

        response = f'CLASS=CONF_MODBUS&ENABLE={enable}&LOCALADDR={localaddr}&'

        for channel in ['M0','M1','M2','M3','M4']:
            enable = d_conf.get('MODBUS',{}).get(channel,{}).get('ENABLE','FALSE')
            name = d_conf.get('MODBUS',{}).get(channel,{}).get('NAME','X')
            sla_addr = str2int(d_conf.get('MODBUS',{}).get(channel,{}).get('SLA_ADDR','0'))
            reg_addr = str2int(d_conf.get('MODBUS',{}).get(channel,{}).get('ADDR','0'))
            nro_regs = str2int(d_conf.get('MODBUS',{}).get(channel,{}).get('NRO_RECS','0'))
            fcode = str2int(d_conf.get('MODBUS',{}).get(channel,{}).get('FCODE','0'))
            mtype = d_conf.get('MODBUS',{}).get(channel,{}).get('TYPE','U16')
            codec = d_conf.get('MODBUS',{}).get(channel,{}).get('CODEC','C0123')
            pow10 = str2int(d_conf.get('MODBUS',{}).get(channel,{}).get('POW10','0'))
            response += f'{channel}={enable},{name},{sla_addr},{reg_addr},{nro_regs},{fcode},{mtype},{codec},{pow10}&'
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
        if 'MODBUS' not in d_conf.keys():
            self.logger.error(f"NO MODBUS in keys !!. Default config.")
            d_rsp = { 'status_code': 200, 'raw_response': 'CLASS=ERROR' }
            return d_rsp
        
        # 2) Calculo el hash de la configuracion de la BD.
        bd_hash = self.get_modbus_hash_from_config(d_conf)
        fx_hash = int(d_params.get('HASH',0), 16)
        self.logger.debug(f"ID={self.dlgid}: BD_hash={bd_hash}, UI_hash={fx_hash}")

        if bd_hash == fx_hash:
            raw_response = 'CLASS=CONF_MODBUS&CONFIG=OK'
            d_rsp = { 'status_code': 200, 'raw_response': raw_response }
            self.logger.debug(f"ID={self.dlgid},RSP=[{raw_response}]")
            return d_rsp
            
        # 3) No coinciden: mando la nueva configuracion
        raw_response = self.get_response_modbus(d_conf)
        d_rsp = { 'status_code': 200, 'raw_response': raw_response }
        self.logger.debug(f"ID={self.dlgid},RSP=[{raw_response}]")
        return d_rsp

