#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from utilidades.str2int import str2int
from utilidades.uhash import u_hash
from usecases.dlg.countersframe_usecase import DlgCountersFrameUsecase


class DlgCountersFrameUsecase_V1(DlgCountersFrameUsecase):
    """
    Se usa en todas las versiones de SPX_AVRDA
    """
    
    def get_counters_hash_from_config(self, d_conf=None):
        '''
        Calculo el hash para la todas las versiones
        '''
        self.logger.debug("V1")

        xhash = 0
        for channel in ['C0','C1']:
            enable =d_conf.get('COUNTERS',{}).get(channel,{}).get('ENABLE','FALSE')
            name = d_conf.get('COUNTERS',{}).get(channel,{}).get('NAME','X')
            modo = d_conf.get('COUNTERS',{}).get(channel,{}).get('MODO','CAUDAL')
            magpp = float(d_conf.get('COUNTERS',{}).get(channel,{}).get('MAGPP','1'))
            rbsize = str2int(d_conf.get('COUNTERS',{}).get(channel,{}).get('RBSIZE','1'))
            hash_str = f'[{channel}:{enable},{name},{magpp:.03f},{modo},{rbsize}]'
            xhash = u_hash(xhash, hash_str)
            #self.logger.debug(f'hash_str={hash_str}')
        return xhash
    
    def get_response_counters(self, d_conf=None):
        '''
        Armo la respuesta para todas las versiones
        '''
        self.logger.debug("V1")
        
        response = 'CLASS=CONF_COUNTERS&'
        for channel in ['C0','C1']:
            enable = d_conf.get('COUNTERS',{}).get(channel,{}).get('ENABLE','FALSE')
            name = d_conf.get('COUNTERS',{}).get(channel,{}).get('NAME', 'X')
            magpp = float(d_conf.get('COUNTERS',{}).get(channel,{}).get('MAGPP', 1.00))
            str_modo = d_conf.get('COUNTERS',{}).get(channel,{}).get('MODO','CAUDAL')
            rbsize = str2int(d_conf.get('COUNTERS',{}).get(channel,{}).get('RBSIZE','1'))
            response += f'{channel}={enable},{name},{magpp},{str_modo},{rbsize}&'
        #
        response = response[:-1]
        return response
    
    
        
 