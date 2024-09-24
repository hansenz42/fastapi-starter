from sqlalchemy import Integer, Column
from component.SqlConnectorManager import sql_connection_manager
from typing import Dict

Base = sql_connection_manager.get_base()


class BasePo(Base):
    """
    基础数据实体
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    def to_dict(self):
        """
        转变为字典
        :return:
        """
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def from_dict(self, dict: Dict):
        """
        从字典中读取
        :param dict:
        :return:
        """
        for key in dict:
            if hasattr(self, key) and dict[key] is not None:
                setattr(self, key, dict[key])
