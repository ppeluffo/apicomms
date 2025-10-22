#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
Genero datos simulando ser un PLC.
"""

import requests

class PlcFrames:

    def __init__(self):
        self.url = 'http://127.0.0.1:5000/apiplc'


    def config(self, id='PLCTEST'):
        params = {'ID':id, 'TYPE': 'PLCV2', 'VER':'1.0.0'}
        data = b'C\xfe\xb1'
        r = requests.post(url=self.url, params=params, data=data, timeout=10)
        print(f"PING TEST(POST): {r.status_code}")


    def ping(self,id='PLCTEST'):
        params = {'ID':id, 'TYPE': 'PLCV2', 'VER':'1.0.0'}
        data = b'P\xe6\xcd'
        r = requests.post(url=self.url, params=params, data=data, timeout=10)
        print(f"PING TEST(POST): {r.status_code}")



if __name__ == '__main__':

    frames = PlcFrames()

    #frames.ping()
    frames.config()
