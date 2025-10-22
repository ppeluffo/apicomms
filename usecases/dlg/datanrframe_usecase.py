#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python


class DlgDataNrFrameUsecase:
    """
    """

    def __init__(self, repo, logger):
        self.repo = repo
        self.logger = logger
        self.dlgid = None
       
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

        #self.logger.debug(f"D_DATALINE={d_dataline}")

        d_rsp = self.repo.save_dataline(unit=self.dlgid, unit_type=unit_type, d_dataline=d_dataline)
        # Aunque haya dado error, continuo para no trancar al datalogger

        d_rsp = { 'status_code': 200, 'raw_response':"" }
        self.logger.debug(f"ID={self.dlgid},d_rsp={d_rsp}")
        return d_rsp


