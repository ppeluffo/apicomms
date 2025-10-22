#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from usecases.oceanus.oceanus_usecase import OceanusFrameUsecase

class OceanusService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger
    
    def procesar_frame(self, unit=None, payload=None):
        """
        No importa la respuesta porque las estaciones OCEANUS no la procesan
        """
        self.logger.debug("")

        d_rsp = OceanusFrameUsecase(self.repo, self.logger).procesar_frame(unit=unit,payload=payload)

        self.logger.debug(f"d_rsp={d_rsp}")
        return d_rsp
