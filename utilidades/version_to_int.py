#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

def version2int (str_version):
    '''
    La version (VER) tiene un formato tipo A.B.C
    A: Funcionalidad
    B: Protocolo
    C: Patch
    Lo convertimos a un numero A*100 + B*10 + 0
    No devolvemos el patch. !!!  
    '''
    components = str_version.split('.')
    try:
        mayor = int(components[0]) * 100
    except:
        mayor = 0

    try:
        minor = int(components[1]) * 10
    except:
        minor = 0

    try:
        patch = int(re.sub(r"[A-Z,a-z,.]",'', components[2]))
    except:
        path = 0

    return mayor + minor
    # return str2int( re.sub(r"[A-Z,a-z,.]",'',str_version))