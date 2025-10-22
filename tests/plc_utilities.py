#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
Genero datos simulando ser un PLC.
"""

import requests
import random
import numpy as np
import struct
from pymodbus.utilities import computeCRC
import pickle
import redis

formato_map = {
    'float': 'f',
    'short': 'h',
    'uchar': 'B'
}

class PlcUtils:

    def __init__(self):
        self.configuracion_mbk = []
        self.datos_mbk = []
        self.respuestas_mbk = []
        self.bytestream = None   # datos serializados de salida
        self.sresp = None
        self.rh = redis.Redis('127.0.0.1')

    def set_plcid(self, id=None):
        self.plcid = id

    def get_configuracion_mbk(self):
        return self.configuracion_mbk
    
    def get_datos_mbk(self):
        return self.datos_mbk
    
    def get_respuestas_mbk(self):
        return self.respuestas_mbk
    
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

        d_config = pickle.loads(pkconfig)
        d_memblock = d_config.get('MEMBLOCK',{})
        self.configuracion_mbk = d_memblock.get('CONFIGURACION',[])
        self.datos_mbk = d_memblock.get('DATOS_PLC',[])
        self.respuestas_mbk = d_memblock.get('DATOS_SRV',[])
        return d_config
        
    def gen_data(self):
        for i in range(len(self.datos_mbk)):
            tipo = self.datos_mbk[i][1]
            val = random.uniform(1,100)
            if tipo == 'short':
                val = np.int16(val)
            elif tipo == 'uchar':
                val = np.int8(val)
            self.datos_mbk[i][2] = val
        return self.datos_mbk

    def gen_bytestream(self):
        
        self.bytestream = b''
        for nombre, formato, valor in self.datos_mbk:
            fmt = formato_map[formato.lower()]
            #print(f"formato={formato}, fmt={fmt}, valor={valor}")
            if fmt == 'h':
                valor = int(valor)
            packed = struct.pack(fmt, valor)
            self.bytestream += packed
        return self.bytestream
    
    def gen_sresp(self):
                
        self.sresp = b'D' + self.bytestream               
        crc = computeCRC(self.sresp)        
        self.sresp += crc.to_bytes(2,'big') 
        return self.sresp
    
    def send_data(self):

        _ = self.gen_data()
        _ = self.gen_bytestream()
        _ = self.gen_sresp()


        crc = computeCRC(self.sresp)
        self.sresp += struct.pack('<H', crc)
        #self.sresp += crc.to_bytes(2,'big')
        print(f"crc={crc}")
        print(f"sresp={self.sresp}")

        try:
            params={'ID':self.plcid, 'TYPE':'PLC','VER':'1.1.0'}
            headers = {"Content-Type": "application/octet-stream"}
            data = self.sresp
            r = requests.post('http://127.0.0.1:5000/apiplc', params=params, data=data, headers=headers, timeout=10 )

        except Exception as e: 
            print( f"Error-> {e}")
            return None
        
        print(self.datos_mbk)
        if r.status_code == 200:
            print(f"RES OK")
            print(f"response={r.content()}")
         
    def desempaquetar(self):

        bytestream = self.sresp[1:-2]
        offset = 0
        for nombre, formato, valor in self.datos_mbk:
            fmt = formato_map[formato]
            size = struct.calcsize(fmt)
            val_unpack = struct.unpack(fmt, bytestream[offset:offset+size])[0]
            print(f'{nombre} -> {val_unpack}')
            offset += size
       
    def unpack_from_mbk(self, bytestream=None, memblock=None):
        """
        Funcion genrica que desempaquete de un memblock dado
        """

        d_payload = {}
        offset = 0
        bytestream = bytestream[1:-2]
        #print(f"bytestream={bytestream}")
        #print(f"MEMBLOCK={memblock}")
        for element in memblock:
            #print(f"ELEMENT={element}")
            nombre, formato, valor = element[:3]
            fmt = formato_map[formato]
            size = struct.calcsize(fmt)
            try:
                val_unpack = struct.unpack(fmt, bytestream[offset:offset+size])[0]
            except Exception as e:
                print(f"Unpack Error {e}")
                return None
            
            d_payload[nombre] = val_unpack
            #print(f'{nombre} -> {val_unpack}')
            offset += size

        return d_payload

    def pack_from_mbk(self, memblock=None):
        """
        """
        #print(f"memblok={memblock}")
        bytestream = b''
        for nombre, formato, valor in memblock:
            fmt = formato_map[formato]
            packed = struct.pack(fmt, valor)
            bytestream += packed
        return bytestream


