#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python


class PlcPingFrameUsecase:
    """
    El frame de ping es:
    payload: b'P\xe6\xcd'
    """

    def __init__(self, logger):
        self.logger = logger
    
    def procesar_frame(self, id=None, payload=None):
        """
        El frame de ping responde igual que lo que recibió.
        """
        self.logger.debug("")

        d_rsp = { 'status_code': 200, 'bytestream': payload }
        return d_rsp
    


