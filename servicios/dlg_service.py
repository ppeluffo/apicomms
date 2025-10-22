#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from usecases.dlg.pingframe_usecase import DlgPingFrameUsecase
from usecases.dlg.recoverframe_usecase import DlgRecoverFrameUsecase
from usecases.dlg.baseframe_usecase import DlgBaseFrameUsecase
from usecases.dlg.baseframe_usecase_V1 import DlgBaseFrameUsecase_V1
from usecases.dlg.ainputsframe_usecase import DlgAinputFrameUsecase
from usecases.dlg.countersframe_usecase import DlgCountersFrameUsecase
from usecases.dlg.countersframe_usecase_V1 import DlgCountersFrameUsecase_V1
from usecases.dlg.modbusframe_usecase import DlgModbusFrameUsecase
from usecases.dlg.consignaframe_usecase import DlgConsignaFrameUsecase
from usecases.dlg.pilotoframe_usecase import DlgPilotoFrameUsecase
from usecases.dlg.flowcontrolframe_usecase import DlgFlowControlFrameUsecase
from usecases.dlg.configallframe_usecase import DlgConfigAllFrameUsecase
from usecases.dlg.datanrframe_usecase import DlgDataNrFrameUsecase
from usecases.dlg.dataframe_usecase import DlgDataFrameUsecase
from usecases.dlg.dataframe_usecase_V1 import DlgDataFrameUsecase_V1

from utilidades.version_to_int import version2int

class DlgService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger
    
    def procesar_frame(self, d_params=None):
        """
        Hago una factoria de usecases
        """
        self.logger.debug("")
      
        clase_frame = d_params.get('CLASS','NONE')
        fw_type = d_params.get('TYPE','NONE')
        ver =  d_params.get('VER','0.0.0')
        fw_ver = version2int(ver)

        #self.logger.debug(f"clase_frame={clase_frame},fw_type={fw_type}, fw_ver={fw_ver}")

        if clase_frame == 'PING':
            d_rsp = DlgPingFrameUsecase(self.logger).procesar_frame(d_params)
        
        elif clase_frame == 'CONF_BASE':
            if fw_type == "SPQ_AVRDA" and fw_ver == 120:
                d_rsp = DlgBaseFrameUsecase_V1(self.repo, self.logger).procesar_frame(d_params)
            else:
                d_rsp = DlgBaseFrameUsecase(self.repo, self.logger).procesar_frame(d_params)

        elif clase_frame == 'CONF_AINPUTS':
            d_rsp =DlgAinputFrameUsecase(self.repo, self.logger).procesar_frame(d_params)

        elif clase_frame == 'CONF_COUNTERS':
            if fw_type == "SPX_AVRDA":
                d_rsp = DlgCountersFrameUsecase_V1(self.repo, self.logger).procesar_frame(d_params)
            else:
                d_rsp = DlgCountersFrameUsecase(self.repo, self.logger).procesar_frame(d_params)

        elif clase_frame == 'CONF_MODBUS':
            d_rsp = DlgModbusFrameUsecase(self.repo, self.logger).procesar_frame(d_params)

        elif clase_frame == 'CONF_CONSIGNA':
            d_rsp = DlgConsignaFrameUsecase(self.repo, self.logger).procesar_frame(d_params)

        elif clase_frame == 'CONF_PILOTO':
            d_rsp = DlgPilotoFrameUsecase(self.repo, self.logger).procesar_frame(d_params)

        elif clase_frame == 'CONF_FLOWC':
            d_rsp = DlgFlowControlFrameUsecase(self.repo,self.logger).procesar_frame(d_params)

        elif clase_frame == 'CONF_ALL':
            d_rsp =DlgConfigAllFrameUsecase(self.repo,self.logger).procesar_frame(d_params)   
            pass

        elif clase_frame == 'RECOVER':
            d_rsp = DlgRecoverFrameUsecase(self.repo, self.logger).procesar_frame(d_params)        
        
        elif clase_frame == 'DATA':
            if fw_type == "FWDLGX" and fw_ver == 110:
                d_rsp = DlgDataFrameUsecase_V1(self.repo, self.logger).procesar_frame(d_params)
            else:
                d_rsp = DlgDataFrameUsecase(self.repo, self.logger).procesar_frame(d_params)

        elif clase_frame == 'DATANR':
            d_rsp = DlgDataNrFrameUsecase(self.repo,self.logger).procesar_frame(d_params)

        else:
            # Catch all errors
            d_rsp = {'status_code': 500, 'raw_response':'FAIL'}

        self.logger.debug(f"d_rsp={d_rsp}")
        return d_rsp
    



    

