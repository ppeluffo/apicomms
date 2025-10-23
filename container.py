#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from servicios.ping_service import PingService
from servicios.oceanus_service import OceanusService
from servicios.plc_service import PlcService
from servicios.dlg_service import DlgService

from repositorios.repodatos import RepoDatos

from datasources.ds_psql.apibdpgsql import ApiBdPgsql
from datasources.ds_redis.apibdredis import ApiBdRedis

from utilidades.login_config import configure_logger

from config import settings

class Container(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(
        modules=["resources.ping_resource",
                 "resources.test_resource",
                 "resources.oceanus_resource",
                 "resources.plc_resource",
                 "resources.dlg_resource",
                 ]
    )
    
    # Logger (singleton compartido)
    logger = providers.Singleton(configure_logger, name="api-comms")

    # Engine y session factory BDLOCAL
    engine_pgsql = providers.Singleton(
        create_engine,
        url=settings.PGSQL_URL, 
        echo=False, 
        isolation_level="AUTOCOMMIT", 
        connect_args={'connect_timeout': 5}
    )

    session_pgsql = providers.Singleton(
        sessionmaker,
        bind = engine_pgsql
    )
    
    # Datasources
    ds_pgsql = providers.Factory( ApiBdPgsql, session_factory = session_pgsql, logger=logger )
    ds_redis = providers.Factory(ApiBdRedis, logger=logger )
    
    # Repositorios
    repo = providers.Factory(RepoDatos, ds_pgsql=ds_pgsql, ds_redis=ds_redis, logger=logger)
        
    # Servicios
    ping_service = providers.Factory(PingService, repositorio=repo, logger=logger)
    oceanus_service = providers.Factory(OceanusService, repositorio=repo, logger=logger)
    plc_service = providers.Factory(PlcService, repositorio=repo, logger=logger)
    dlg_service = providers.Factory(DlgService, repositorio=repo, logger=logger)
    




