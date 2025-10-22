#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import re
from datetime import datetime

NEEDLES_LIST = ['HUM:[0-9.]+', 'TEMPER:[0-9.]+', 'PM10:[0-9.]+', 'PM2.5:[0-9.]+', 'TSP:[0-9.]+', 'AIRPRE:[0-9.]+']

class OceanusFrameUsecase:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger

    def filtrar_payload(self, payload=None):
        """
        OJO QUE LOS barraF dan error por eso les puse \\F
        Filtra el contenido recibido en POST y solo se queda con los bytes imprimibles.
        Convierto el rx_payload para solo quedarme con los ascii.
        rx_payload=b'\x00\x00\x18\x00\x0c\x00\x0c\x00\x01\n\x01\x02\x00\x00\x00\x00\x01\x01\x01\x00\x17\x02\x11\x00\x00\x00\\FO000HUM:47.0%RH\xcc
             \xffZ\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\x01\x00\x00\x80\x00\x00\x00\x00\x00\x00\xfe\x02:\x00\xa3\x06\x02\x00\x00\x00\x011\x00\x00
             \x00\x00$\x00\x0c\x00\x0c\x00\x02\n\x01\x02\x00\x00\x00\x00\x01\x01\x01\x00\x17\x02\x16\x00\x00\x00\\FO000AIRPRE:1016.0hPaJrZ'

        payload = 7.\\FO000TEMPER:24.3HZ5
        payload = \\FO000PM10:29.0ug/m3KZ7.$\\FO000TSP:78.0ug/m3nZ

        HUM:47.0%
        AIRPRE:1016.0hPa            
        TEMPER:24.1
        """
        self.logger.debug("")

        clean_payload = ''
        for i in payload:
            if 33 <= i <= 127:
                clean_payload += chr(i)

        return clean_payload        

    def extract_mags_values_from_payload(self, clean_payload=None):
        """
        Revisa el string clean_payload ( solo caracteres imprimibles ) y extra los nombres y valores de las magnitudes
        que las devuelve en d_mags.
        payload = 7.\\FO000TEMPER:24.3HZ5
        { TEMPER = 24.3 }
        """
        self.logger.debug("")

        d_mags = {}
        for needle in NEEDLES_LIST:
            subs = re.search(needle,clean_payload)
            if subs:
                s = subs.group()
                name,value = s.split(':')
                d_mags[name] = value
        
        self.logger.debug(f"d_mags={d_mags}")
        return d_mags
    
    def procesar_frame(self, unit=None, payload=None):
        """
        No importa la respuesta porque las estaciones OCEANUS no la procesan
        """
        self.logger.debug("")

        #self.logger.debug(f"payload={payload}")
        clean_payload = self.filtrar_payload(payload)
        d_mags = self.extract_mags_values_from_payload(clean_payload)
        # Agregamos las key de DATE/TIME que no trae
        now = datetime.now()
        d_mags['DATE'] = now.strftime('%y%m%d')
        d_mags['TIME'] = now.strftime('%H%M%S')

        self.logger.debug(f"d_mags={d_mags}")
        _ =  self.repo.save_dataline(unit=unit, unit_type='OCEANUS', d_dataline=d_mags)

        d_rsp = {'status_code':200}
        return d_rsp
    
    

