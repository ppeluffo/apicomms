#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python


class DlgPingFrameUsecase:
    """
    El frame de ping es:
    payload: b'P\xe6\xcd'
    """

    def __init__(self, logger):
        self.logger = logger
    
    def procesar_frame(self, d_params=None):
        """
        """
        self.logger.debug("")

        d_rsp = { 'status_code': 200, 'raw_response': 'CLASS=PONG' }
        return d_rsp
    


