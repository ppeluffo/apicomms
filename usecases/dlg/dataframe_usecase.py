#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from datetime import datetime
from flask import current_app

class DlgDataFrameUsecase:
    """
    """

    def __init__(self, repo, logger):
        self.repo = repo
        self.logger = logger
        self.dlgid = None
       
    def preparar_raw_response( self, ordenes=None):
        now=datetime.now().strftime('%y%m%d%H%M')
        raw_response = f'CLASS=DATA&CLOCK={now}'
        if ordenes:
            raw_response += f';{ordenes}'
        return raw_response
    
    def procesar_frame(self, d_params=None):
        """
        """
        self.logger.debug("")
 
        #self.logger.debug(f"D_PARAMS={d_params}")

        self.dlgid = d_params.get('ID',None)
        if self.dlgid is None:
            self.logger.info(f"ERROR dlgid None")
            return {'status_code':400}
 
        unit_type = d_params.get('TYPE','None')
        # Elimino todos los campos que no son datos
        d_dataline = d_params
        _ = d_dataline.pop('ID',None)
        _ = d_dataline.pop('HW',None)
        _ = d_dataline.pop('TYPE',None)
        _ = d_dataline.pop('VER',None)
        _ = d_dataline.pop('CLASS',None)

        if current_app.config["UNIT_ID"] == current_app.config["DEBUG_ID"]:
            self.logger.info(f"ID={current_app.config['UNIT_ID']}: D_DATALINE={d_dataline}")

        d_rsp = self.repo.save_dataline(unit=self.dlgid, unit_type=unit_type, d_dataline=d_dataline)
        
        # Aunque haya dado error, continuo para no trancar al datalogger
        # Proceso las ordenes
        ordenes = None
        d_rsp = self.repo.read_ordenes(unit=self.dlgid)
        assert isinstance(d_rsp, dict)
        if d_rsp.get('status_code',0) == 200:
            ordenes = d_rsp['d_ordenes']

            # Si RESET entonces borro la configuracion en Redis
            if 'RESET' in ordenes:
                _ = self.repo.delete_configuracion_unidad(unit=self.dlgid)
            #
            # Borro las ordenes
            _ = self.repo.delete_ordenes(unit=self.dlgid)

        raw_response = self.preparar_raw_response(ordenes)

        d_rsp = { 'status_code': 200, 'raw_response': raw_response }
        return d_rsp
    


