#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python3


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, JSON, Double
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import pytz # For creating timezone-aware datetime objects

import os

API_VERSION = os.environ.get('API_VERSION','R002 @ 2025-09-30')
#
PGSQL_HOST = os.environ.get('PGSQL_HOST', '127.0.0.1')
PGSQL_PORT = os.environ.get('PGSQL_PORT','5435')
PGSQL_USER = os.environ.get('PGSQL_USER', 'admin')
PGSQL_PASSWD = os.environ.get('PGSQL_PASSWD', 'pexco599')
PGSQL_BD = os.environ.get('PGSQL_BD','bd_spcomms')

PGSQL_URL = f"postgresql+psycopg2://{PGSQL_USER}:{PGSQL_PASSWD}@{PGSQL_HOST}:{PGSQL_PORT}/{PGSQL_BD}"

engine_bdlocal = create_engine(url=PGSQL_URL, echo=False, isolation_level="AUTOCOMMIT", connect_args={'connect_timeout': 5})
Session_bdlocal = sessionmaker(bind=engine_bdlocal)
session_bdlocal = Session_bdlocal()


Base_local = declarative_base()

class Historica(Base_local):

    __tablename__ = 'historica'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    fechadata = Column(DateTime(timezone=False), nullable=True, default=datetime.now())
    fechasys = Column(DateTime(timezone=False), nullable=True, default=datetime.now())
    equipo = Column(String(50), nullable=False, index=True)
    tag = Column(String(50), nullable=True)
    valor = Column(Double)

    def __init__(self, fechadata, fechasys, equipo, tag, valor):
        self.fechadata = fechadata
        self.fechasys = fechasys
        self.equipo = equipo
        self.tag = tag
        self.valor = valor

    def __repr__(self):
        return f'Datos({self.equipo}, {self.tag}, {self.fechadata}, {self.fechasys}, {self.valor})'

    def __str__(self):
        return f'Datos({self.equipo}, {self.tag}, {self.fechadata}, {self.fechasys}, {self.valor})'
    
class Online(Base_local):

    __tablename__ = 'online'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    fechadata = Column(DateTime(timezone=False), nullable=True, default=datetime.now())
    fechasys = Column(DateTime(timezone=False), nullable=True, default=datetime.now())
    equipo = Column(String(50), nullable=False, index=True)
    tag = Column(String(50), nullable=True)
    valor = Column(Double)

    def __init__(self, fechadata, fechasys, equipo, tag, valor):
        self.fechadata = fechadata
        self.fechasys = fechasys
        self.equipo = equipo
        self.tag = tag
        self.valor = valor

    def __repr__(self):
        return f'Datos({self.equipo}, {self.tag}, {self.fechadata}, {self.fechasys}, {self.valor})'

    def __str__(self):
        return f'Datos({self.equipo}, {self.tag}, {self.fechadata}, {self.fechasys}, {self.valor})'
    
class Configuraciones(Base_local):

    __tablename__ = 'configuraciones'

    pk = Column( Integer(), primary_key=True, autoincrement=True)
    unit_id = Column(String(20), nullable=True, default='NONE')
    uid = Column(String(50), nullable=True, default='')
    jconfig = Column( JSON() )

    def __init__(self, unit_id, uid='', jconfig=''):
        self.unit_id = unit_id
        self.uid = uid
        self.jconfig = jconfig

    def __repr__(self):
        return f'Configuracion({self.unit_id}, {self.uid}, {self.jconfig})'

    def __str__(self):
        return self.unit_id
    
class Usuarios(Base_local):

    __tablename__ = 'usuarios'

    user_id = Column(String(30), primary_key=True, nullable=False)
    fecha_ultimo_acceso = Column(DateTime(timezone=False), nullable=True, default=datetime.now())
    data_ptr = Column(Integer())
    label = Column(String(300), nullable=True)
 
    def __init__(self, user_id, label):
        self.user_id = user_id
        self.fecha_ultimo_acceso = None
        self.data_ptr = 0
        self.label = label

    def __repr__(self):
        return f'Usuario({self.user_id}, {self.fecha_ultimo_acceso}, {self.data_ptr}, {self.label})'

    def __str__(self):
        return self.user_id
        #return f'Usuario({self.user_id}, {self.fecha_ultimo_acceso}, {self.data_ptr}, {self.label})'

class RecoverId(Base_local):

    __tablename__ = 'recoverid'

    uid = Column(String(50), primary_key=True, nullable=False)
    id = Column(String(30), nullable=False)
 
    def __init__(self, uid, id):
        self.uid = uid
        self.id = id

    def __repr__(self):
        return f'RecoverId({self.uid}, {self.id})'

    def __str__(self):
        return self.uid
        #return f'Usuario({self.user_id}, {self.fecha_ultimo_acceso}, {self.data_ptr}, {self.label})'


def create_all():
    print("Creando base...")
    Base_local.metadata.create_all(engine_bdlocal )

if __name__ == "__main__":
    create_all()
