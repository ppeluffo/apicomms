#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python3

def str2int(s):
    '''
    Convierte un string a un nro.entero con la base correcta.
    '''
    if not isinstance(s, str):
        return 0
    if 'X' in s.upper():
        return int(s,16)
    return int(s)