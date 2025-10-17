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

        d_rsp1 =  self.repo.ping_apiredis()
        d_rsp2 =  self.repo.ping_apidatos()

        if d_rsp1.get('status_code', 0) == 200:
            json1 = d_rsp1.get('json')
        else:
            json1 = {}

        if d_rsp2.get('status_code', 0) == 200:
            json2 = d_rsp2.get('json')
        else:
            json2 = {}
        
        d_rsp = { 'status_code':200,
                  'apiredis_status_code': d_rsp1['status_code'],
                 'apiredis_params': json1,
                 'apidatos_status_code': d_rsp2['status_code'],
                 'apidatos_params': json2,
                   }
        
        return d_rsp
    

