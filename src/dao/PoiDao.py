from component.SqlConnectorManager import sql_connection_manager
from entity.po.PoiPo import PoiPo

class PoiDao:
    def __init__(self):
        self.__session_maker = sql_connection_manager.get_session_maker()