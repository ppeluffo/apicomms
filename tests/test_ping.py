#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
Genero datos simulando ser un PLC.
"""

import requests

class Ping:

    def __init__(self, id='PLCTEST', tipo='PLCV2', ver='1.0.0'):
        self.url = 'http://127.0.0.1:5000//apicomms/ping'
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
        params = {'ID':id, 'TYPE': 'PLCV2', 'VER':'1.0.0'}
        data = b'P\xe6\xcd'
        r = requests.get(url=self.url, params=params, data=data, timeout=10)
        print(f"PING TEST(GET): {r.status_code}")

if __name__ == '__main__':

    ping = Ping()
    ping.send_frame()

