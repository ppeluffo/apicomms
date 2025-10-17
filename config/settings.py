#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python3

import os

#
API_VERSION = os.environ.get('API_VERSION','R002 @ 2025-09-30')
#
API_REDIS_HOST = os.environ.get('API_REDIS_HOST','127.0.0.1')
API_REDIS_PORT = os.environ.get('API_REDIS_PORT','5100')
API_REDIS_URLBASE = f"http://{API_REDIS_HOST}:{API_REDIS_PORT}/apiredis"

API_DATOS_HOST = os.environ.get('API_PGSQL_HOST','127.0.0.1')
API_DATOS_PORT = os.environ.get('API_PGSQL_PORT','5300')
API_DATOS_URLBASE = f"http://{API_DATOS_HOST}:{API_DATOS_PORT}/apidatos"

# DEBUG->INFO->ERROR
LOG_LEVEL = os.environ.get('LOG_LEVEL','INFO')



