#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python3

import pickle
import datetime as dt

class RepoDatos:
    """
    Repositorio que se encarga de consultar las apis de redis y datossql
    """
    
    def __init__(self, ds_pgsql, ds_redis, logger):
        self.ds_pgsql = ds_pgsql
        self.ds_redis = ds_redis
        self.logger = logger

    def ping_redis(self):
        """
        """
        self.logger.debug("")
        return self.ds_redis.ping()
    
    def ping_pgsql(self):
        """
        """
        self.logger.debug("")
        return self.ds_pgsql.ping()
        
    #####################################################################################

    def save_dataline(self, unit=None, unit_type=None, d_dataline=None):
        """
        Al recibir un dataline se hacen 3 funciones:
        - Se guarda en el HSET de la unidad
        - Se guarda el timestamp en el HSET TIMESTAMP. Este nos permite saber cuando llegaron el ultimo dato de c/unidad
        - Se guarda en una cola de datos recibidos RXDATA_QUEUE.
        """
        self.logger.debug("")

        # Timestamp: Indica la fecha/hora de recibido el dato.
        timestamp = dt.datetime.now()
        try:
            pk_timestamp = pickle.dumps(timestamp)
        except Exception as e:
            self.logger.error( f"Error->{e}")
            d_rsp = {'status_code':502, 'msg':f"{e}"}
            return d_rsp
        #
        # pk_dataline: Los datos recibidos se guardan y encolan en forma serializada pickle
        try:
            pk_dataline = pickle.dumps(d_dataline)
        except Exception as e:
            self.logger.error( f"Error->{e}")
            d_rsp = {'status_code':502, 'msg':f"{e}"}
            return d_rsp
        #
        # pk_datastruct: Estructura de datos serializada que se encola en RXDATA_QUEUE
        d_datastruct = {'TYPE':unit_type, 'ID':unit, 'D_LINE':d_dataline}
        try:
            pk_datastruct = pickle.dumps(d_datastruct)
        except Exception as e:
            self.logger.error( f"Error->{e}")
            d_rsp = {'status_code':502, 'msg':f"{e}"}
            return d_rsp
        #
        # Debemos hacer 3 operaciones en la redis:

        # 1. Guardamos los datos en el HSET de la unidad
        d_rsp = self.ds_redis.save_dataline(unit, pk_dataline)
        if d_rsp.get('status_code',0) != 200:
            return d_rsp
        
        # 2. Guardamos el timestamp
        d_rsp = self.ds_redis.save_timestamp(unit, pk_timestamp)
        if d_rsp.get('status_code',0) != 200:
            return d_rsp
        
        # 3. Encolo todos los datos en RXDATA_QUEUE para luego procesarlos y pasarlos a pgsql.
        d_rsp = self.ds_redis.enqueue_dataline(unit, pk_datastruct)
        if d_rsp.get('status_code',0) != 200:
            return d_rsp
                
        return d_rsp

    def leer_configuracion_unidad(self, unit_id=None):
        """
        Le pide la configuracion a REDIS.
        Si no existe la pide a PGSQL y si este la devuelve, actualiza REDIS
        Si no existe ni en redis ni en pgsql, devuelve error.
        """
        self.logger.debug("")

        d_rsp = self.ds_redis.read_configuracion_unidad(unit_id)
        assert isinstance(d_rsp, dict)

        status_code = d_rsp.get('status_code', 500)
        if d_rsp.get('status_code',0) == 200:
            # pkconfig es un string
            pkconfig = d_rsp.get('pkconfig', '')
            try:
                d_config = pickle.loads(pkconfig)
                #self.logger.debug(f"Redis d_config={d_config}")
                assert isinstance(d_config, dict)
                d_rsp = {'status_code':200, 'd_config': d_config }
                
            except Exception as e:
                self.logger.error( f"ConfigService:read_config: {e}")
                d_rsp = {'status_code':502, 'msg':f"{e}"}

            self.logger.debug(f"Config found in Redis")
            return d_rsp
        
        # La configuracion NO esta en la redis: busco en la pgsql
        d_rsp = self.ds_pgsql.read_configuracion_unidad(unit_id)
        assert isinstance(d_rsp, dict)
        
        status_code = d_rsp.get('status_code', 500)
        if status_code == 200:
            # La BD devuelve una tupla !!
            d_config = d_rsp['jconfig_raw'][0]
            #self.logger.debug(f"Pgsql d_config={d_config}")
            assert isinstance(d_config, dict)
            d_rsp = { 'status_code':200, 'd_config': d_config}

            # La configuracion estaba en la pgsql: actualizo la redis
            self.logger.debug(f"configuracion en pgsql: d_rsp={d_rsp}")

            try:
                pkconfig = pickle.dumps(d_config)
            except Exception as e:
                self.logger.error( f"ConfigService:update_config: {e}")
                d_rsp = {'status_code':502, 'msg':f"{e}"}
                return d_rsp

            self.logger.debug(f"Config found in Pgsql")
            _ = self.ds_redis.set_configuracion_unidad(unit_id, pkconfig)
            return d_rsp
        
        # Aqui es que no hay configuracion
        #d_rsp = {'status_code':404, 'd_config': {} }
        return d_rsp

    #####################################################################################

    def read_ordenesplc(self, unit=None):
        """.
        """
        self.logger.debug("")

        d_rsp = self.ds_redis.read_ordenesplc(unit=unit)
        if d_rsp.get('status_code',0) == 200:
            pk_ordenes_plc = d_rsp['pk_ordenes_plc']
            try:
                d_ordenes_plc = pickle.loads(pk_ordenes_plc) 
                d_rsp = {'status_code':200, 'd_ordenes_plc':d_ordenes_plc}
                
            except Exception as e:
                self.logger.error( f"Error-> {e}")
                d_rsp = {'status_code':502, 'msg':f"{e}"}

        return d_rsp
    
    def delete_ordenesplc(self, unit=None):
        """.
        """
        self.logger.debug("")

        return self.ds_redis.delete_ordenesplc(unit=unit)
 
    def read_dataline(self, unit=None):
        """
        Leemos una dataline de REDIS.
        """
        self.logger.debug("")

        d_rsp =  self.ds_redis.read_dataline(unit=unit)
        if d_rsp.get('status_code',0) == 200:
            pk_dataline = d_rsp['pk_dataline']
            try:
                d_dataline = pickle.loads(pk_dataline) 
                d_rsp = {'status_code':200, 'd_dataline':d_dataline}

            except Exception as e:
                self.logger.error( f"Error-> {e}")
                d_rsp = {'status_code':502, 'msg':f"{e}"}

        return d_rsp
    
    #####################################################################################

    def update_uid2id( self, id=None, uid=None):
        """
        Leo el uidid de redis. Si coincide salgo.
        Si no actualizo en redis y en pgsql
        """
        self.logger.debug("")  

        d_rsp = self.get_id_from_uid(uid)
        if d_rsp.get('status_code',0 ) != 200:
            # No esta.
            _ = self.ds_redis.set_id_and_uid(uid=uid, id=id)
            _ = self.ds_pgsql.set_id_and_uid(uid=uid, id=id)
        d_rsp = {'status_code':200}
        return d_rsp
    
    def get_id_from_uid(self, uid=None):
        """.
        """
        self.logger.debug("")

        # 1. Le pregunto a Redis por uid->id
        d_rsp = self.ds_redis.get_id_from_uid(uid)
        assert isinstance(d_rsp, dict)

        status_code = d_rsp.get('status_code', 0)
        if status_code == 200:
            return d_rsp
        
        # 2. No esta en Redis: pregunto a SQL
        d_rsp = self.ds_pgsql.get_id_from_uid(uid)
        assert isinstance(d_rsp, dict)

        status_code = d_rsp.get('status_code', 0)
        if status_code == 200:
            # Actualizo la redis
            id = d_rsp.get('id','')
            _ = self.ds_redis.set_id_and_uid(uid, id)
            return d_rsp
        
        # No esta en Redis ni en SQL: Error.
        d_rsp = { 'status_code': 400 }
        return d_rsp
    
    def update_commsparameters( self, d_conf=None):
        """
        """
        self.logger.debug("")     

        imei = d_conf.get('IMEI',None)
        iccid = d_conf.get('ICCID',None)
        type = d_conf.get('TYPE',None)
        ver = d_conf.get('VER',None)

        #print(f'DEBUG d_args={d_args}')
        #_ = update_comms_conf( self.d_args, {'DLGID':dlgid, 'TYPE':type, 'VER':ver, 'UID':uid, 'IMEI':imei, 'ICCID':iccid})
        d_rsp = {'status_code':200}
        return d_rsp
    
    #####################################################################################

    def read_ordenes(self, unit=None):
        """.
        """
        self.logger.debug("")

        d_rsp = self.ds_redis.read_ordenes(unit=unit)
        if d_rsp.get('status_code',0) == 200:
            pk_ordenes = d_rsp['pk_ordenes']
            try:
                d_ordenes = pickle.loads(pk_ordenes) 
                d_rsp = {'status_code':200, 'd_ordenes':d_ordenes }
                
            except Exception as e:
                self.logger.error( f"Error-> {e}")
                d_rsp = {'status_code':502, 'msg':f"{e}"}

        return d_rsp
    
    def delete_ordenes(self, unit=None):
        """.
        """
        self.logger.debug("")

        return self.ds_redis.delete_ordenes(unit=unit)
 
     #####################################################################################

    def delete_configuracion_unidad(self, unit_id=None):
        """.
        """
        self.logger.debug("")

        return self.ds_redis.delete_configuracion_unidad(unit_io=unit_id)
    
    