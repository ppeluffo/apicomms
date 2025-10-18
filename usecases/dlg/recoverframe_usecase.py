#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python


class DlgRecoverFrameUsecase:
    """
    Le pregunto al repositorio si con el uid me puede dar el id.
    El repo ve si esta en Redis o SQL pero a mi, aca esto no me importa.
    Lo resuelve el repo.
    """

    def __init__(self, repo, logger):
        self.repo = repo
        self.logger = logger
    
    def procesar_frame(self, d_params=None):
        """
        """
        self.logger.debug("")

        uid = d_params.get('UID','')
        
        d_rsp = self.repo.get_id_from_uid(uid)
        
        status_code = d_rsp.get('status_code',0)
        if status_code == 200:
            id = d_rsp.get('id','')
            d_rsp = { 'status_code': 200, 'raw_response': f"CLASS=RECOVER&ID={id}" }
        else:
            d_rsp = { 'status_code': 200, 'raw_response': 'CONFIG=ERROR' }
            
        return d_rsp



