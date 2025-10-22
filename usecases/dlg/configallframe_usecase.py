#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from utilidades.str2int import str2int
from utilidades.uhash import u_hash

from usecases.dlg.baseframe_usecase import DlgBaseFrameUsecase
from usecases.dlg.ainputsframe_usecase import DlgAinputFrameUsecase
from usecases.dlg.countersframe_usecase import DlgCountersFrameUsecase
from usecases.dlg.modbusframe_usecase import DlgModbusFrameUsecase
from usecases.dlg.consignaframe_usecase import DlgConsignaFrameUsecase
from usecases.dlg.flowcontrolframe_usecase import DlgFlowControlFrameUsecase

class DlgConfigAllFrameUsecase:
    """
    ID=SPQTEST&HW=SPQ_AVRDA_R1&TYPE=FWDLGX&VER=1.0.4&CLASS=CONF_ALL&UID=42419193000040100136011800000000&IMEI=868191051472973&
        ICCID=8959801019445151129F&CSQ=73&WDG=32&BH=0x42&AH=0xA4&CH=0xBC&MH=0x2B&PH=0x15
    """

    def __init__(self, repo, logger):
        self.repo = repo
        self.logger = logger
        self.dlgid = None
    
        
    def procesar_frame(self, d_params=None):
        """
        """
        self.logger.debug("")
 
        self.dlgid = d_params.get('ID',None)
        if self.dlgid is None:
            self.logger.info(f"ERROR dlgid None")
            return {'status_code':400}

        # 1) Chequeo la causa de la conexion
        wdg = int(d_params.get('WDG',-1))
        if (wdg & 0x01) != 0:
            self.logger.info(f"{self.dlgid} RESET CAUSE PORF")
        elif (wdg & 0x02) != 0:
            self.logger.info(f"{self.dlgid} RESET CAUSE BORF")
        elif (wdg & 0x04) != 0:
            self.logger.info(f"{self.dlgid} RESET CAUSE EXTF")
        elif (wdg & 0x08) != 0:
            self.logger.info(f"{self.dlgid} RESET CAUSE WDRF")
        elif (wdg & 0x10) != 0:
            self.logger.info(f"{self.dlgid} RESET CAUSE SWRF")
        else:
            self.logger.info(f"{self.dlgid} RESET CAUSE UNKNOWN")

        # 2) Le pido al repositorio que me de la configuracion
        d_rsp = self.repo.leer_configuracion_unidad(self.dlgid)
        assert isinstance(d_rsp, dict)
        self.logger.debug(f"id={self.dlgid}, d_rsp={d_rsp}")
        
        if d_rsp.get('status_code',0) != 200:
            self.logger.error(f"CONFIG ERROR")
            d_rsp = { 'status_code': 200, 'raw_response': 'CLASS=CONF_ALL&CONFIG=ERROR' }
            return d_rsp
 
        d_conf = d_rsp['d_config']
 
        # 2) Actualizo uid2id
        uid = d_params.get('UID',None)
        _ = self.repo.update_uid2id( self.dlgid, uid)

        # 3) Actualizo los parámetros de comunicaciones
        _ = self.repo.update_commsparameters(d_params)

        # 4) Calculo el hash de la configuracion de la BD.
        raw_response = 'CLASS=CONF_ALL'
        new_conf = False

        # BASE
        bd_Bhash = DlgBaseFrameUsecase(self.repo, self.logger).get_base_hash_from_config(d_conf)
        if bd_Bhash != int(d_params.get('BH','-1'),16):
            raw_response += '&BASE'
            new_conf = True
            self.logger.debug(f"id={self.dlgid}: Config BASE")
        
        # ANALOG
        bd_Ahash = DlgAinputFrameUsecase(self.repo, self.logger).get_ainputs_hash_from_config(d_conf)
        if bd_Ahash != int(d_params.get('AH','-1'),16):
            raw_response += '&AINPUTS'
            new_conf = True
            self.logger.debug(f"id={self.dlgid}: Config ANALOG")

        # COUNTER
        bd_Chash = DlgCountersFrameUsecase(self.repo, self.logger).get_counters_hash_from_config(d_conf)

        if bd_Chash != int(d_params.get('CH','-1'),16):
            raw_response += '&COUNTER'
            new_conf = True
            self.logger.debug(f"id={self.dlgid}: Config COUNTER")

        # MODBUS
        bd_Mhash = DlgModbusFrameUsecase(self.repo, self.logger).get_modbus_hash_from_config(d_conf)
        if bd_Mhash != int(d_params.get('MH','-1'),16):
            raw_response += '&MODBUS'
            new_conf = True
            self.logger.debug(f"id={self.dlgid}: Config MODBUS")

        # PRESION
        bd_Phash = DlgConsignaFrameUsecase(self.repo, self.logger).get_consigna_hash_from_config(d_conf)
        if bd_Phash != int(d_params.get('PH','-1'),16):
            raw_response += '&PRESION'
            new_conf = True
            self.logger.debug(f"id={self.dlgid}: Config PRESION")

        # FLOWCONTROL
        bd_Fhash = DlgFlowControlFrameUsecase(self.repo, self.logger).get_flowcontrol_hash_from_config(d_conf)
        if bd_Fhash != int(d_params.get('FH','-1'),16):
            raw_response += '&FLOWC'
            new_conf = True
            self.logger.debug(f"id={self.dlgid}: Config FLOWC")
        
        if not new_conf:
            raw_response += '&CONFIG=OK'

        d_rsp = { 'status_code': 200, 'raw_response': raw_response }
        self.logger.debug(f"ID={self.dlgid},RSP=[{raw_response}]")
        return d_rsp

