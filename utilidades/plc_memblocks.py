#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python3

from collections import namedtuple
from struct import unpack_from, pack
from pymodbus.utilities import computeCRC
import numpy as np
import struct

formato_map = {
    'float': 'f',
    'short': 'h',
    'uchar': 'B'
}

class Memblock:
    """
    Defino los objetos memblock que se usan en las comunicaciones de los PLC
    """
    def __init__(self, logger):

        self.logger = logger
        self.plcid = None
        self.configuracion_mbk = []
        self.datos_mbk = []
        self.respuestas_mbk = []
        self.tx_bytestream = None   # datos serializados de salida

    def set_plcid(self, id):
        """
        """
        self.logger.debug("")

        self.plcid = id

    def set_memblock(self, d_memblock=None):
        """
        """
        self.logger.debug("")

        self.configuracion_mbk = d_memblock.get('CONFIGURACION',[])
        self.datos_mbk = d_memblock.get('DATOS_PLC',[])
        self.respuestas_mbk = d_memblock.get('DATOS_SRV',[])

    def get_respuestas_mbk(self):
        return self.respuestas_mbk

    ##############################################################

    def unpack_from_mbk(self, bytestream=None, memblock=None):
        """
        Funcion genrica que desempaquete de un memblock dado
        """
        self.logger.debug("")

        d_payload = {}
        offset = 0
        for nombre, formato, valor in memblock:
            fmt = formato_map[formato]
            size = struct.calcsize(fmt)
            try:
                val_unpack = struct.unpack(fmt, bytestream[offset:offset+size])[0]
            except Exception as e:
                self.logger.info(f"Unpack Error {e}")
                return None
            
            d_payload[nombre] = val_unpack
            self.logger.debug(f'{nombre} -> {val_unpack}')
            offset += size
            
        return d_payload
        
    def unpack_from_datosmbk(self, bytestream=None ):
        """
        """
        self.logger.debug("")
    
        return self.unpack_from_mbk(bytestream, self.datos_mbk)

    def pack_from_mbk(self, memblock=None):
        """
        """
        self.logger.debug("")

        bytestream = b''
        for nombre, formato, valor in memblock:
            fmt = formato_map[formato]
            packed = struct.pack(fmt, valor)
            bytestream += packed
        return bytestream

    def pack_from_configmbk(self):
        """
        """
        self.logger.debug("")

        return self.pack_from_mbk(self.configuracion_mbk)

    def check_payload_crc_valid(self, rx_bytes):
        '''
        Calcula el CRC del payload y lo compara el que trae.
        El payload trae el CRC que envia el PLC en los 2 ultimos bytes
        El payload es un bytestring
        '''
        self.logger.debug("")
        crc = int.from_bytes(rx_bytes[-2:],'big')
        calc_crc = computeCRC(rx_bytes[:-2])
        if crc == calc_crc:
            return True
        else:
            return False
 