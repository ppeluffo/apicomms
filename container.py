#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from dependency_injector import containers, providers

from servicios.ping_service import PingService
from servicios.oceanus_service import OceanusService
from servicios.plc_service import PlcService

from repositorios.repodatos import RepoDatos

from datasources.ds_apidatos.apidatos import Apidatos
from datasources.ds_apiredis.apiredis import Apiredis

from utilidades.login_config import configure_logger

from config import settings

class Container(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(
        modules=["resources.ping_resource",
                 "resources.test_resource",
                 "resources.oceanus_resource",
                 "resources.plc_resource",

                 ]
    )
    
    # Logger (singleton compartido)
    logger = providers.Singleton(configure_logger, name="api-redis")

    # Datasources
    ds_apidatos = providers.Factory(Apidatos, logger=logger )
    ds_apiredis = providers.Factory(Apiredis, logger=logger )
    
    # Repositorios
    repo = providers.Factory(RepoDatos, ds_apidatos=ds_apidatos, ds_apiredis=ds_apiredis, logger=logger)
        
    # Servicios
    ping_service = providers.Factory(PingService, repositorio=repo, logger=logger)
    oceanus_service = providers.Factory(OceanusService, repositorio=repo, logger=logger)
    plc_service = providers.Factory(PlcService, repositorio=repo, logger=logger)
    




