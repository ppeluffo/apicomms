#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import multiprocessing

max_requests = 1000
max_requests_jitter = 50

# Si queremos el log en stdout

#workers = multiprocessing.cpu_count() * 2 + 1
workers = 10

# Enviar logs a stdout/stderr
accesslog = '-'      # stdout
errorlog = '-'       # stderr
loglevel = 'info'

# Opcional: formato de access log
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
#acceslogformat = ""
