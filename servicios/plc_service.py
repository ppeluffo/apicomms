#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from usecases.plc.pingframe_usecase import PlcPingFrameUsecase
from usecases.plc.configframe_usecase import PlcConfigFrameUsecase
from usecases.plc.dataframe_usecase import PlcDataFrameUsecase

class PlcService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger
    
    def read_debug_id(self):
        #self.logger.debug("")
        return self.repo.read_debug_id()
    
    def procesar_frame(self, unit_id=None, payload=None):
        """
        No importa la respuesta porque las estaciones OCEANUS no la procesan
        """
        self.logger.debug("")

        # El primer byte del payload de los PLC indica el tipo de frame
        # 80: (P) ping
        # 67: (C) configuracion
        # 68: (D) data
        id_frame = payload[0]

        if id_frame == 80:
            d_rsp = PlcPingFrameUsecase(self.logger).procesar_frame(unit_id=unit_id, payload=payload)  

        elif id_frame == 67:
            d_rsp = PlcConfigFrameUsecase(self.repo, self.logger).procesar_frame(unit_id=unit_id, payload=payload)

        elif id_frame == 68:
            d_rsp = PlcDataFrameUsecase(self.repo, self.logger).procesar_frame(unit_id=unit_id, payload=payload)

        else:
            self.logger.error(f"PLC unit_id={unit_id} error de id_frame {id_frame}")
            d_rsp = { 'status_code': 400 }

        #self.logger.debug(f"d_rsp={d_rsp}")
        return d_rsp
    


    

