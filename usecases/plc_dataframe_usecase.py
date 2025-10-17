#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python


from utilidades.plc_memblocks import Memblock
from pymodbus.utilities import computeCRC
from datetime import datetime
import struct

class PlcDataFrameUsecase:
    """
    Procesamos los frames de configuracion.
    Sirven para enviarle parámetros operativos al PLC

    El frame de data es:
    rx_payload: b'D\x00\x00\x00\x00\x8f\xc2\xf5<\xc8K\x07@\x1f` F31 Ff\x00\xcc\xcc\xc6?\x00\x00\x00\x00\x85\xeb
                   \xd1>\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00{\x14\x1e@\x00\x7fz'
    rsp: b'D\xd6\x02\x00\x00\x01\x00\x01\x00\x00 \xc1\x00\x01{\x14\x1e@{\x14\x1e@"\xc2'

    """

    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger
        self.mbk = Memblock(self.logger)
    
    ############################################################
    
    def procesar_data_reception(self, id=None, payload=None):
        """
        Proceso la recepcion de datos.
        Debo usar el datos_mbk.
        Desempaqueto el bytestream recibido de acuerdo al datos_mbk. 
        [
            ['UPA1_CAUDALIMETRO', 'float', 32.15],['UPA1_STATE1', 'uchar', 100],['UPA1_POS_ACTUAL_6', 'short', 24],
            ['UPA2_CAUDALIMETRO', 'float', 11.5],['BMB_STATE18', 'uchar', 201]
        ]
        """
        self.logger.debug("")

        # 1) El CRC debe ser correcto. Lo debo calcular con todos los bytes (inclusive el 'D')
        if not self.mbk.check_payload_crc_valid(payload):
            self.logger.debug(f"id={id}, rx_payload CRC Error")
            return {'status_code': 400}
        #
        # 2) Elimino el primer caracter y los 2 últimos (crc)
        bytestream = payload[1:-2]
        #
        # 3) Desempaqueto el bytestream de acuerdo al formato indicado en datos_mbk
        d_payload = self.mbk.unpack_from_datosmbk(bytestream)
        if d_payload is None:
            return {'status_code': 400}
        
        # 4) Agrego los campos DATE y TIME para normalizarlos a la BD.
        # 'DATE': '230417', 'TIME': '161057'
        now = datetime.now()
        d_payload['DATE'] = now.strftime('%y%m%d')
        d_payload['TIME'] = now.strftime('%H%M%S')
        #self.logger.debug(f"id={id}, d_payload={d_payload}")

        # 5. Guardo los datos recibidos
        d_rsp = self.repo.save_plc_dataline(id, d_payload)

        return d_rsp    

    ############################################################
    def helper_generate_sys_val(self, nombre):
        '''
        Por ahora solo es para el TIMESTAMP
        '''
        self.logger.debug("")

        if nombre == 'TIMESTAMP':
            now = datetime.now()
            now_str = now.strftime("%H%M")
            return int(now_str)
        #
        return 0

    def helper_read_ordenesplc(self,id=None):
        """
        """
        self.logger.debug("")
        d_rsp = self.repo.read_ordenesplc(unit=id)
        assert isinstance(d_rsp, dict)
        if d_rsp.get('status_code',0) == 200:
            d_ordenes_plc = d_rsp.get('d_ordenes_plc',{})
        else:
            d_ordenes_plc = {}
    
        return d_ordenes_plc
    
    def helper_generate_remote_val(self, def_val, origen, rem_name ):
        """
        """
        self.logger.debug("")

        d_rsp = self.repo.read_dataline(unit=origen)
        if d_rsp.get('status_code',0) == 200:
            d_dataline = d_rsp.get('d_dataline',{})
            val = float(d_dataline.get(rem_name, def_val))
        else:
            val = def_val
        return val

    def preparar_data_response(self, id=None):
        """
        Genero el bytestream para enviar de vuelta al PLC
        Las respuestas se mandan de acuerdo al respuestas_mbk
        En este se indica para c/respuesta de donde procede, su tipo y formato.
        """
        self.logger.debug("")

        l_resposes_mbk = []
        l_respuestas_mbk = self.mbk.get_respuestas_mbk()
        self.logger.debug(f"l_respuestas_mbk={l_respuestas_mbk}")

        # Para no leer en c/variable las ordenes, la leo una sola vez y las borro
        d_ordenes_plc = self.helper_read_ordenesplc(id)
        _ = self.repo.delete_ordenesplc(id)

        for (nombre,tipo,def_val,origen,rem_name) in l_respuestas_mbk:
            if origen == 'SYS':
                val = self.helper_generate_sys_val(nombre)
            
            elif origen == 'ATVISE':
                val = d_ordenes_plc.get(nombre, def_val)
                borrar_orden_atvise = True
        
            else:
                val = self.helper_generate_remote_val(def_val, origen, rem_name )   
                 
            l_resposes_mbk.append( [nombre, tipo, val ])

        self.logger.debug(f"l_responses_mbk={l_resposes_mbk}")

        bytestream = self.mbk.pack_from_mbk(l_resposes_mbk)
        d_rsp = {'status_code': 200, 'bytestream': bytestream }
        return d_rsp

    ############################################################           
    
    def procesar_frame(self, id=None, payload=None):
        """
        -Proceso primero la recepcion
        -Luego preparo la respuesta.
        """
        self.logger.debug("")
        
        # 1) Le pido al repositorio que me de la configuracion
        d_rsp = self.repo.leer_configuracion_plc(id)
        assert isinstance(d_rsp, dict)
        #self.logger.debug(f"id={id}, d_rsp={d_rsp}")
        
        if d_rsp.get('status_code',0) != 200:
            d_rsp = { 'status_code':400 }
            return d_rsp
        
        d_memblock = d_rsp.get('d_config',{}).get('MEMBLOCK',{})
        self.logger.debug(f"id={id}, d_memblock={d_memblock}")

        # 2) El memblok de la configuracion se lo paso al mbk helper que instancie en el init.
        self.mbk.set_plcid(id)                      # Carglo el plcid
        self.mbk.set_memblock(d_memblock)           # Cargo la configuracion

        # 3) Proceso los datos: Los extraigo de bytestream y los inserto en la bd(redis)   
        d_rsp = self.procesar_data_reception(id, payload)
        #self.logger.debug(f"id={id}, d_rsp={d_rsp}")
        if d_rsp.get('status_code',0) != 200:
            d_rsp = { 'status_code':400 }
            return d_rsp
        
        # 4) Genero la respuesta
        d_rsp = self.preparar_data_response(id)
        self.logger.debug(f"id={id}, d_rsp={d_rsp}")
        if d_rsp.get('status_code',0) != 200:
            d_rsp = { 'status_code':400 }
        
        bytestream = b'D' + d_rsp.get('bytestream',b'')   # El primer byte debe ser un 'D' ( data )
        crc = computeCRC(bytestream)                 # Calculo el CRC
        bytestream += struct.pack('<H', crc)         # Lo agrego al final convertido antes en bytes
        
        d_rsp = { 'status_code': 200, 'bytestream': bytestream }
        return d_rsp

    
