#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

class PingService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger

    def ping(self):
        """
        Vemos que tanto la interfaz con ApiRedis como con ApiDatos esten activas
        """
        self.logger.debug("")

        d_rsp_redis =  self.repo.ping_redis()
        d_rsp_pgsql =  self.repo.ping_pgsql()

        d_rsp = { 'status_code':200,
                  'redis': d_rsp_redis,
                  'pgsql': d_rsp_pgsql
                   }
        
        return d_rsp
    

