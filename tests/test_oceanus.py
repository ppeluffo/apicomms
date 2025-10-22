#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
Genero datos simulando ser un PLC.
"""

import requests

class Oceanus:

    def __init__(self, id='EM01', tipo='OCEANUS', ver='1.0.0'):
        self.url = 'http://127.0.0.1:5000/apioceanus'
        self.id = id
        self.tipo = tipo
        self.ver = ver

    def set_id(self, id=None):
        self.id = id

    def set_type(self, tipo=None):
        self.tipo = tipo

    def set_ver(self, ver=None):
        self.ver = ver

    def send_frame(self):
        params = {'ID':id, 'TYPE': 'OCEANUS', 'VER':'1.0.0'}
        data = b'\x00\x00\x18\x00\x0c\x00\x0c\x00\x01\n\x01\x02\x00\x00\x00\x00\x01\x01\x01\x00\x17\x02\x11\x00\x00\x00\\FO000HUM:47.0%RH\xcc\xffZ\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\x01\x00\x00\x80\x00\x00\x00\x00\x00\x00\xfe\x02:\x00\xa3\x06\x02\x00\x00\x00\x011\x00\x00\x00\x00$\x00\x0c\x00\x0c\x00\x02\n\x01\x02\x00\x00\x00\x00\x01\x01\x01\x00\x17\x02\x16\x00\x00\x00\\FO000AIRPRE:1016.0hPaJrZ'
        r = requests.post(url=self.url, params=params, data=data, timeout=10)
        print(f"OCEANUS TEST(POST): {r.status_code}")

if __name__ == '__main__':

    oceanus = Oceanus()
    oceanus.send_frame()

