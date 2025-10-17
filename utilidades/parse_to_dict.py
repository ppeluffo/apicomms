#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import json
import ast

"""
Muchas veces el json que viene en un request no tiene el formato adecuado, por
ej. por no tener las comillas adecuados y esto hace que al convertirlo a objeto
de error.
Esta funcion se encarga de corregirlo
"""
def parse_to_dict(raw_value):

    if not raw_value:
        return {}
    
    if isinstance(raw_value, dict):
        return raw_value
    
    try:
        return json.loads(raw_value)
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(raw_value)
        except (ValueError, SyntaxError):
            return {}
        