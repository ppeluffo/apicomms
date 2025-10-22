#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
Genero datos simulando ser un PLC.
"""

import argparse
import requests
import random
import pickle
import pprint
import redis

class Dlg:

    def __init__(self, id='DLGTEST', tipo='FWDLGX', ver='1.0.0'):
        self.rh = redis.Redis('127.0.0.1')
        self.url = 'http://127.0.0.1:5000/apidlg'
        self.id = id
        self.tipo = tipo
        self.ver = ver
        self.d_config = None

    def parse_get_response(self, text_response=None):
        text_response = text_response.replace('<html>','')
        text_response = text_response.replace('</html>','')
        text_response = text_response.replace('\n','')
        text_response = text_response.replace('"','')
        l_fields = text_response.split('&')
        return l_fields
    
    def read_config_from_redis(self, id=None):
        """
        El equipo debe estar configurado en REDIS
        """          
        try:
            pkconfig = self.rh.hget( id, 'PKCONFIG')
            if pkconfig is None:
                return None

        except Exception as e:
            print( f"Redis Error {e}")
            return None

        self.d_config = pickle.loads(pkconfig)
        return self.d_config
    
    def send_frame(self, class_frame=None, params=None):
        r = requests.get(url=self.url, params=params, timeout=10)
        print(f"{class_frame} TEST(GET): {r.status_code}")
        if r.status_code == 200:
            print(f"RESPONSE: {r.text}")
            l_fields = self.parse_get_response(r.text)
            pprint.pprint(l_fields)

    def send_ping_frame(self):
        params = {'ID':self.id, 'TYPE': self.tipo, 'VER': self.ver, 'CLASS':'PING'}
        self.send_frame('PING', params)

    def send_base_frame_V0(self):
        params = {'ID':self.id, 
                  'TYPE': self.tipo, 
                  'VER': self.ver, 
                  'CLASS':'CONF_BASE',
                  'UID':'123456789ABC', 
                  'IMEI':'868191051472973', 
                  'ICCID':'8959801019445151129F',
                  'CSQ':'73',
                  'WDG':'32',
                  'HASH':'0x01'
                  }
        self.send_frame('BASE', params)

    def send_base_frame_V1(self):
        params = {'ID':self.id, 
                  'TYPE': 'SPQ_AVRDA', 
                  'VER': '1.2.1', 
                  'CLASS':'CONF_BASE',
                  'UID':'42419193000040100136011800000000', 
                  'IMEI':'868191051472973', 
                  'ICCID':'8959801019445151129F',
                  'CSQ':'73',
                  'WDG':'32',
                  }
        self.send_frame('BASE', params)

    def send_ainputs_frame(self):
        params = {'ID':self.id, 'TYPE': self.tipo, 'VER': self.ver, 'CLASS':'CONF_AINPUTS','HASH':'0x01'}
        self.send_frame('AINPUTS', params)

    def send_counters_frame_V0(self):
        params = {'ID':self.id, 'TYPE': self.tipo, 'VER': self.ver, 'CLASS':'CONF_COUNTERS','HASH':'0x01'}
        self.send_frame('COUNTERS', params)

    def send_counters_frame_V1(self):
        params = {'ID':self.id, 'TYPE': 'SPX_AVRDA', 'VER': '1.2.1', 'CLASS':'CONF_COUNTERS','HASH':'0x01'}
        self.send_frame('COUNTERS', params)

    def send_modbus_frame(self):
        params = {'ID':self.id, 'TYPE': 'SPX_AVRDA', 'VER': '1.2.1', 'CLASS':'CONF_MODBUS','HASH':'0x01'}
        self.send_frame('MODBUS', params)

    def send_consigna_frame(self):
        params = {'ID':self.id, 'TYPE': 'SPX_AVRDA', 'VER': '1.2.1', 'CLASS':'CONF_CONSIGNA','HASH':'0x01'}
        self.send_frame('CONSIGNA', params)

    def send_piloto_frame(self):
        params = {'ID':self.id, 'TYPE': 'SPX_AVRDA', 'VER': '1.2.1', 'CLASS':'CONF_PILOTO','HASH':'0x01'}
        self.send_frame('PILOTO', params)

    def send_flowc_frame(self):
        params = {'ID':self.id, 'TYPE': 'SPX_AVRDA', 'VER': '1.2.1', 'CLASS':'CONF_FLOWC','HASH':'0x01'}
        self.send_frame('FLOWC', params)

    def send_configall_frame(self):
        params = {'ID':self.id, 
                  'TYPE': 'SPX_AVRDA', 
                  'VER': '1.2.1', 
                  'CLASS':'CONF_ALL',
                  'UID':'42419193000040100136011800000000', 
                  'IMEI':'868191051472973', 
                  'ICCID':'8959801019445151129F',
                  'CSQ':'73',
                  'WDG':'32',
                  'BH':'0x41',
                  'AH':'0xA3',
                  'CH':'0xBB',
                  'MH': '0x2A', 
                  'PH': '0x14',
                  'FH':'0x11'
                  }
        
        self.send_frame('CONF_ALL', params)

    def send_recover_frame(self):
        params = {'ID': 'DEFAULT', 
                  'TYPE': self.tipo, 
                  'VER': self.ver, 
                  'CLASS':'RECOVER',
                  'UID':'123456789ABC'
                  }
        self.send_frame('RECOVER', params)

    def send_datanr_frame(self):
        params = {'ID':'DLGTEST',
                  'HW':'SPQ_AVRDA',
                  'TYPE':'FWDLGX',
                  'VER':'1.0.0',
                  'CLASS':'DATANR',
                  'DATE':'230321',
                  'TIME':'094504',
                  'PA':'1.20',
                  'PB':'3.40',
                  'PC':'0.56',
                  'Q0':'32.100',
                  'Q1':'12.800',
                  'bt':'12.496'                
                  }
        
        self.send_frame('DATANR', params)

    def send_data_frame_V0(self):
        params = {'ID':'DLGTEST',
                  'HW':'SPQ_AVRDA',
                  'TYPE':'FWDLGX',
                  'VER':'1.0.0',
                  'CLASS':'DATA',
                  'DATE':'230321',
                  'TIME':'094504',
                  'PA':'1.20',
                  'PB':'3.40',
                  'PC':'0.56',
                  'Q0':'32.100',
                  'Q1':'12.800',
                  'bt':'12.496'                
                  }
        
        self.send_frame('DATA', params)

    def send_data_frame_V1(self):
        params = {'ID':'DLGTEST',
                  'HW':'SPQ_AVRDA',
                  'TYPE':'FWDLGX',
                  'VER':'1.1.0',
                  'CLASS':'DATA',
                  'DATE':'230321',
                  'TIME':'094504',
                  'PA':'1.20',
                  'PB':'3.40',
                  'PC':'0.56',
                  'Q0':'32.100',
                  'Q1':'12.800',
                  'bt':'12.496'                
                  }
        
        self.send_frame('DATA', params)


def make_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--frame", type=str, 
                        choices=['ping', 'base0', 'base1', 'ainputs', 'counters0', 'counters1',
                                 'modbus', 'consigna','piloto', 'flowc','configall','recover',
                                 'datanr','data0','data1'] )
    return parser
                                   
if __name__ == '__main__':

    parser = make_arguments()
    args = parser.parse_args()

    dlg = Dlg()

    if args.frame == 'ping':
        dlg.send_ping_frame()
    elif args.frame == 'base0':
        dlg.send_base_frame_V0()
    elif args.frame == 'base1':
        dlg.send_base_frame_V1()
    elif args.frame == 'ainputs':
        dlg.send_ainputs_frame()
    elif args.frame == 'counters0':
        dlg.send_counters_frame_V0()
    elif args.frame == 'counters1':
        dlg.send_counters_frame_V1()
    elif args.frame == 'modbus':
        dlg.send_modbus_frame()  
    elif args.frame == 'consigna':  
        dlg.send_consigna_frame() 
    elif args.frame == 'piloto': 
        dlg.send_piloto_frame()
    elif args.frame == 'flowc':
        dlg.send_flowc_frame()
    elif args.frame == 'configall':
        dlg.send_configall_frame()
    elif args.frame == 'recover':
        dlg.send_recover_frame()
    elif args.frame == 'datanr':
        dlg.send_datanr_frame()
    elif args.frame == 'data0':
        dlg.send_data_frame_V0()
    elif args.frame == 'data1':
        dlg.send_data_frame_V1()

