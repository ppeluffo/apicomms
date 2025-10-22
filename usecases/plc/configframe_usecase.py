#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python


from utilidades.plc_memblocks import Memblock
from pymodbus.utilities import computeCRC
import struct

class PlcConfigFrameUsecase:
    """
    Procesamos los frames de configuracion.
    Sirven para enviarle parámetros operativos al PLC

    El frame de config es:
    payload: b'C\xfe\xb1'

    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger
        self.mbk = Memblock(self.logger)
    
    def procesar_frame(self, unit_id=None, payload=None):
        """
        -Leo la configuracion del PLC desde el repositorio
        -Genero un memblock con el template de la configuracion
        -Serializo el memblock y lo envio
        """
        self.logger.debug("")
        
        # Le pido al repositorio que me de la configuracion
        d_rsp = self.repo.leer_configuracion_unidad(unit_id)
        assert isinstance(d_rsp, dict)
        #self.logger.debug(f"unit_id={unit_id}, d_rsp={d_rsp}")

        if d_rsp.get('status_code',0) != 200:
            d_rsp = { 'status_code':400 }
            return d_rsp
        
        d_memblock = d_rsp.get('d_config',{}).get('MEMBLOCK',{})
        self.logger.debug(f"unit_id={unit_id}, d_memblock={d_memblock}")

        # El memblok de la configuracion se lo paso al mbk helper que instancie en el init.
        self.mbk.set_plcid(unit_id)                 # Carglo el plcid
        self.mbk.set_memblock(d_memblock)           # Cargo la configuracion

        bytestream = self.mbk.pack_from_configmbk()  # Lo transformo en bytesting
        bytestream = b'C' + bytestream               # El primer byte debe ser un 'C' ( configuracion )
        crc = computeCRC(bytestream)                 # Calculo el CRC
        bytestream += struct.pack('<H', crc)         # Lo agrego al final convertido antes en bytes
        #sresp += crc.to_bytes(2,'big')          .
        
        #self.logger.debug(f'id={id}, bytestream={bytestream}')
        d_rsp = { 'status_code': 200, 'bytestream': bytestream }
        return d_rsp

