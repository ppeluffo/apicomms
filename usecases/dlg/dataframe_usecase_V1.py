#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from usecases.dlg.dataframe_usecase import DlgDataFrameUsecase

from datetime import datetime

class DlgDataFrameUsecase_V1(DlgDataFrameUsecase):
    """
    """

    def preparar_raw_response( self, ordenes=None):
        now=datetime.now().strftime('%y%m%d%H%M') + str(datetime.now().isoweekday())
        raw_response = f'CLASS=DATA&CLOCK={now}'
        if ordenes:
            raw_response += f';{ordenes}'
        return raw_response


    




