#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python3

class RepoDatos:
    """
    Repositorio que se encarga de consultar las apis de redis y datossql
    """
    
    def __init__(self, ds_apidatos, ds_apiredis, logger):
        self.ds_apidatos = ds_apidatos
        self.ds_apiredis = ds_apiredis
        self.logger = logger
        
    def ping_apiredis(self):
        """
        """
        self.logger.debug("")
        return self.ds_apiredis.ping()
    
    def ping_apidatos(self):
        """
        """
        self.logger.debug("")
        return self.ds_apidatos.ping()

    def save_oceanus_dataline(self,id=None,d_mags=None):
        """
        La apiredis espera en el entrypoint /dataline un dict con la
        key 'dataline'
        """
        self.logger.debug("")
        jparams = { 'dataline': d_mags }

        tipo='OCEANUS'
        _ = self.ds_apiredis.put_dataline(id=id, tipo=tipo, jparams=jparams)

    def save_plc_dataline(self,id=None, d_mags=None):
        """
        La apiredis espera en el entrypoint /dataline un dict con la
        key 'dataline'
        """
        self.logger.debug("")
        jparams = { 'dataline': d_mags }
        tipo='PLC'
        return self.ds_apiredis.put_dataline(id=id, tipo=tipo, jparams=jparams)

    def leer_configuracion(self, id=None):
        """
        Le pide la configuracion a REDIS.
        Si no existe la pide a PGSQL y si este la devuelve, actualiza REDIS
        Si no existe ni en redis ni en pgsql, devuelve error.
        """
        self.logger.debug("")

        d_rsp = self.ds_apiredis.read_configuration(id)
        assert isinstance(d_rsp, dict)

        status_code = d_rsp.get('status_code', 500)
        if status_code == 200:
            # La configuracion esta en la redis
            #self.logger.debug(f"configuracion en redis: d_rsp={d_rsp}")
            return d_rsp
        
        # La configuracion NO esta en la redis: busco en la pgsql
        d_rsp = self.ds_apidatos.read_configuration(id)
        assert isinstance(d_rsp, dict)
        
        status_code = d_rsp.get('status_code', 500)
        if status_code == 200:
            # La configuracion estaba en la pgsql: actualizo la redis
            self.logger.debug(f"configuracion en pgsql: d_rsp={d_rsp}")
            d_config = d_rsp.get('d_config',{})
            _ = self.ds_apiredis.set_configuration(id, d_config)
            return d_rsp
        
        # Aqui es que no hay configuracion
        #d_rsp = {'status_code':404, 'd_config': {} }
        return d_rsp
    
    def read_dataline(self, unit=None):
        """
        Leemos una dataline de REDIS.
        """
        self.logger.debug("")

        return self.ds_apiredis.read_dataline(unit=unit)

    def read_ordenesplc(self, unit=None):
        """.
        """
        self.logger.debug("")

        return self.ds_apiredis.read_ordenesplc(unit=unit)
    
    def delete_ordenesplc(self, unit=None):
        """.
        """
        self.logger.debug("")

        return self.ds_apiredis.delete_ordenesplc(unit=unit)
    
    def get_id_from_uid(self, uid=None):
        """.
        """
        self.logger.debug("")

        # 1. Le pregunto a Redis por uid->id
        d_rsp = self.ds_apiredis.get_uid2id(uid)
        assert isinstance(d_rsp, dict)

        status_code = d_rsp.get('status_code', 0)
        if status_code == 200:
            return d_rsp
        
        # 2. No esta en Redis: pregunto a SQL
        d_rsp = self.ds_apidatos.get_uid2id(uid)
        assert isinstance(d_rsp, dict)

        status_code = d_rsp.get('status_code', 0)
        if status_code == 200:
            # Actualizo la redis
            id = d_rsp.get('id','')
            _ = self.ds_apiredis.update_uid2id(uid, id)
            return d_rsp
        
        # No esta en Redis ni en SQL: Error.
        d_rsp = { 'status_code': 400 }
        return d_rsp
    
    def update_uid2id( self, id=None, uid=None):
        """
        Leo el uidid de redis. Si coincide salgo.
        Si no actualizo en redis y en pgsql
        """
        self.logger.debug("")  

        d_rsp = self.get_id_from_uid(uid)
        if d_rsp.get('status_code',0 ) != 200:
            # No esta.
            _ = self.ds_apiredis.set_uid2id(uid=uid, id=id)
            _ = self.ds_apidatos.set_uid2id(uid=uid, id=id)
        d_rsp = {'status_code':200}
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
    
