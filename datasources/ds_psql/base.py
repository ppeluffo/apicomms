#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python3

from deprecated_apidatos.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine_bdlocal = create_engine(url=settings.PGSQL_URL, echo=False, isolation_level="AUTOCOMMIT", connect_args={'connect_timeout': 5})
Session_bdlocal = sessionmaker(bind=engine_bdlocal)
session_bdlocal = Session_bdlocal()

Base_local = declarative_base()
