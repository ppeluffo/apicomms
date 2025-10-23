#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from utilidades.str2int import str2int
from utilidades.uhash import u_hash
from flask import current_app
from utilidades.selective_logger import slogger

class DlgFlowControlFrameUsecase:
    """
    """

    def __init__(self, repo, logger):
        self.repo = repo
        self.logger = logger
        self.dlgid = None
    
    def get_flowcontrol_hash_from_config(self, d_conf=None):
        '''
        '''
        self.logger.debug("")

        xhash = 0
        enable = d_conf.get('FLOWCONTROL',{}).get('ENABLE','FALSE')
        hash_str = f'[{enable.upper()}]'
        xhash = u_hash(xhash, hash_str)
        #
        for channel in range(14):
            slot_name = f'SLOT{channel}'
            s_dow = d_conf.get('FLOWCONTROL',{}).get(slot_name,{}).get('DOW','--')
            s_dow = s_dow.upper()
            if s_dow == 'LU':
                dow = 1;
            elif s_dow == 'MA':
                dow = 2
            elif s_dow == 'MI':
                dow = 3
            elif s_dow == 'JU':
                dow = 4
            elif s_dow == 'VI':
                dow = 5
            elif s_dow == 'SA':
                dow = 6
            elif s_dow == 'DO':
                dow = 7
            else:
                dow = 8

            ptime = str2int( d_conf.get('FLOWCONTROL',{}).get(slot_name,{}).get('TIME','0000') )
            action = d_conf.get('FLOWCONTROL',{}).get(slot_name,{}).get('ACTION','CLOSE')

            hash_str = f'[SLOT{channel:02d}:{dow:02d},{ptime:04d},{action.upper()}]'
            xhash = u_hash(xhash, hash_str)
            #self.logger.debug(f'hash_str={hash_str}{xhash}')
        # 
        return xhash
    
    def get_response_flowcontrol(self, d_conf=None):
        '''
        '''
        self.logger.debug("")
        
        enable = d_conf.get('FLOWCONTROL',{}).get('ENABLE','FALSE')
        response = f'CLASS=CONF_FLOWC&ENABLE={enable}'
        #
        for channel in range(14):
            slot_name = f'SLOT{channel}'
            s_dow = d_conf.get('FLOWCONTROL',{}).get(slot_name,{}).get('DOW','--')
            s_dow = s_dow.upper()
            if s_dow == 'LU':
                dow = 1;
            elif s_dow == 'MA':
                dow = 2
            elif s_dow == 'MI':
                dow = 3
            elif s_dow == 'JU':
                dow = 4
            elif s_dow == 'VI':
                dow = 5
            elif s_dow == 'SA':
                dow = 6
            elif s_dow == 'DO':
                dow = 7
            else:
                dow = 8

            ptime = str2int( d_conf.get('FLOWCONTROL',{}).get(slot_name,{}).get('TIME','0000') )
            action = d_conf.get('FLOWCONTROL',{}).get(slot_name,{}).get('ACTION','CLOSE')
            response += f'&S{channel:02d}:{s_dow},{ptime:04d},{action.upper()}'
        #
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
        if 'FLOWCONTROL' not in d_conf.keys():
            self.logger.error(f"NO FLOWCONTROL in keys !!. Default config.")
            d_rsp = { 'status_code': 200, 'raw_response': 'CLASS=ERROR' }
            return d_rsp
        
        # 2) Calculo el hash de la configuracion de la BD.
        bd_hash = self.get_flowcontrol_hash_from_config(d_conf)
        fx_hash = int(d_params.get('HASH',0), 16)
        slogger(f"BD_hash={bd_hash}, UI_hash={fx_hash}")

        if bd_hash == fx_hash:
            raw_response = 'CLASS=CONF_FLOWCONTROL&CONFIG=OK'
            d_rsp = { 'status_code': 200, 'raw_response': raw_response }
            return d_rsp
            
        # 3) No coinciden: mando la nueva configuracion
        raw_response = self.get_response_flowcontrol(d_conf)
        d_rsp = { 'status_code': 200, 'raw_response': raw_response }
        return d_rsp

