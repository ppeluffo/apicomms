#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
Genero datos simulando ser un PLC.
"""

import requests
from plc_utilities import PlcUtils
import struct
from pymodbus.utilities import computeCRC
import pprint
import argparse

class Plc:

    def __init__(self, id='PLCTEST', tipo='PLC', ver='1.0.0'):
        self.url = 'http://127.0.0.1:5000/apiplc'
        self.id = id
        self.tipo = tipo
        self.ver = ver
        self.plcutils = PlcUtils()

    def set_id(self, id=None):
        self.id = id

    def set_tipo(self, tipo=None):
        self.tipo = tipo

    def set_ver(self, ver=None):
        self.ver = ver

    def send_frame_ping(self):
        params = {'ID':self.id, 'TYPE':self.tipo , 'VER':self.ver}
        data = b'P\xe6\xcd'
        print(f'SEND')
        r = requests.post(url=self.url, params=params, data=data, timeout=10)
        print(f"PLC PING TEST(POST): {r.status_code}")
        print(f"RESPONSE: {r.content}")

    def send_frame_config(self):
        params = {'ID':self.id, 'TYPE':self.tipo , 'VER':self.ver}
        data = b'C\xfe\xb1'
        print(f'SEND')
        r = requests.post(url=self.url, params=params, data=data, timeout=10)
        print(f"PLC CONFIG TEST(POST): {r.status_code}")
        print(f"RESPONSE: {r.content}")
        
        # Procesamos la respuesta
        bytestream = r.content
        #
        if not self.plcutils.read_config_from_redis(self.id):
            print(f"Error: PLC {self.id} no esta configurado en Redis")
            return
        conf_mbk = self.plcutils.get_configuracion_mbk()
        print(f'CONF_MBK={conf_mbk}')
        d_config_data = self.plcutils.unpack_from_mbk(bytestream, conf_mbk)
        print()
        print(f'DATA={d_config_data}')

    def send_frame_data(self):
        if not self.plcutils.read_config_from_redis(self.id):
            print(f"Error: PLC {self.id} no esta configurado en Redis")
            return
        _ = self.plcutils.gen_data()
        _ = self.plcutils.gen_bytestream()
        sresp = self.plcutils.gen_sresp()

        crc = computeCRC(sresp)
        sresp += struct.pack('<H', crc)
        #print(f"crc={crc}")
        #print(f"sresp={sresp}")

        try:
            params = {'ID':self.id, 'TYPE':self.tipo , 'VER':self.ver}
            headers = {"Content-Type": "application/octet-stream"}
            data = sresp
            print(f'SEND')
            r = requests.post(url=self.url, params=params, data=data, headers=headers, timeout=10 )

        except Exception as e: 
            print( f"Error-> {e}")
            return None
        
        # Datos enviados serializados
        print(f"DATOS ENVIADOS:")
        pprint.pprint(self.plcutils.datos_mbk)
        
        if r.status_code == 200:
            print(f"RES OK")
            print(f"response={r.content}")
            bytestream = r.content
            d_payload = self.plcutils.unpack_from_mbk(bytestream, self.plcutils.respuestas_mbk)
            pprint.pprint(d_payload)

def make_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--frame", type=str, 
                        choices=['ping', 'config', 'data'] )
    return parser


if __name__ == '__main__':

    parser = make_arguments()
    args = parser.parse_args()

    plc = Plc()
    plc.set_id = 'PLCTEST'
    plc.set_tipo = 'PLC'
    plc.set_ver = '1.0.0'

    if args.frame == 'ping':
        plc.send_frame_ping()
    elif args.frame == 'config':
        plc.send_frame_config()
    elif args.frame == 'data':
        plc.send_frame_data()


