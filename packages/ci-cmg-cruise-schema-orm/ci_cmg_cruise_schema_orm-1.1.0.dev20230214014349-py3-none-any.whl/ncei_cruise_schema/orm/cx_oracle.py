import oracledb
from .persistence import PersistenceEngine

class CxOraclePersistenceEngine(PersistenceEngine):
  def __init__(
      self,
      host,
      port,
      service_name,
      user,
      password,
      schema="cruise",
      debug_query=False,
      debug_params=False,
      threaded=False,
      pooled_connection=False
  ):
    self.__user = user
    self.__password = password
    self.__dsn = oracledb.makedsn(host, port, service_name=service_name)
    self.__debug_query = debug_query
    self.__debug_params = debug_params
    self.__threaded = threaded
    if schema:
      self.__schema = schema + "."
    else:
      self.__schema = ""
    if pooled_connection:
      self.__pool = oracledb.create_pool()
    else:
      self.__pool = None

  def _debug_query(self):
    return self.__debug_query

  def _debug_params(self):
    return self.__debug_params

  def _schema(self):
    return self.__schema

  def _placeholder_func(self, name):
    return ":" + name

  def _get_connection(self):
    if self.__pool:
      return self.__pool.acquire()
    return oracledb.connect(user=self.__user, password=self.__password, dsn=self.__dsn)

  def _set_clob(self, value):
    if type(value) == oracledb.LOB:
      return value.read()
    return value
