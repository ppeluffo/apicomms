#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python3

import os

#
API_VERSION = os.environ.get('API_VERSION','R002 @ 2025-09-30')
#
#PGSQL_HOST = os.environ.get('PGSQL_HOST', '192.168.0.8')
#PGSQL_PORT = os.environ.get('PGSQL_PORT','5432')
PGSQL_HOST = os.environ.get('PGSQL_HOST', '127.0.0.1')
PGSQL_PORT = os.environ.get('PGSQL_PORT','5435')
PGSQL_USER = os.environ.get('PGSQL_USER', 'admin')
PGSQL_PASSWD = os.environ.get('PGSQL_PASSWD', 'pexco599')
PGSQL_BD = os.environ.get('PGSQL_BD','bd_spcomms')
PGSQL_URL = f"postgresql+psycopg2://{PGSQL_USER}:{PGSQL_PASSWD}@{PGSQL_HOST}:{PGSQL_PORT}/{PGSQL_BD}"

BDREDIS_HOST = os.environ.get('BDREDIS_HOST','127.0.0.1')
BDREDIS_PORT = os.environ.get('BDREDIS_PORT','6379')
BDREDIS_DB = os.environ.get('BDREDIS_DB','0')


# DEBUG->INFO->ERROR
LOG_LEVEL = os.environ.get('LOG_LEVEL','INFO')



