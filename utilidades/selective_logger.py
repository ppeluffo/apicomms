#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python3

import inspect
from flask import current_app

def slogger(s):

    from container import Container  # 💡 import diferido (lazy)
    logger = Container.logger()

    #caller = inspect.currentframe().f_back.f_code.co_name
    frame = inspect.currentframe().f_back
    #caller = f"{frame.f_globals['__name__']}.{frame.f_code.co_name}"
    caller = f"{frame.f_code.co_name}"

    if logger.level < 20 or ( current_app.config["UNIT_ID"] == current_app.config["DEBUG_ID"] ):
        logger.info(f"[{caller}] [{current_app.config['UNIT_ID']}]: {s}")
