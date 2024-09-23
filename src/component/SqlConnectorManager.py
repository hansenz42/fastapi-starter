import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from component.ConfigManager import config_manager
from urllib.parse import quote_plus
from sqlalchemy.pool import NullPool


class SQLConnectionManager:
    def __init__(self):
        if config_manager.get_value('env') in ['dev', 'test']:
            # 为测试环境禁用连接池，防止 eventloop 错误
            self.engine = create_async_engine(
                config_manager.get_value('sql', 'url') % quote_plus(config_manager.get_value('sql', 'password')),
                poolclass=NullPool,
            )
        else:
            self.engine = create_async_engine(
                config_manager.get_value('sql', 'url') % quote_plus(config_manager.get_value('sql', 'password')),
                poolclass=NullPool,
            )
        self.session_maker = async_sessionmaker(bind=self.engine, expire_on_commit=True)
        self.base_obj = sqlalchemy.ext.declarative.declarative_base()

    def make_session(self):
        """
        创建数据库会话
        :return:
        """
        return self.session_maker()

    def get_session_maker(self):
        """
        获取数据库会话生成器
        :return:
        """
        return self.session_maker

    def get_base(self):
        """
        获取数据库基类
        :return:
        """
        return self.base_obj


sql_connection_manager: SQLConnectionManager = SQLConnectionManager()

import sys

if 'pytest' in sys.modules:
    import pytest

    @pytest.mark.asyncio
    async def test_init_session_maker():
        session_maker = sql_connection_manager.get_session_maker()

        # select some data from database session
        async with session_maker() as session:
            # run select * from poi
            result = await session.execute(sqlalchemy.text("select * from poi"))
            print(result.fetchall())
