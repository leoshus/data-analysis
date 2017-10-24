#-*- coding=utf-8 -*-
import MySQLdb
from MySQLdb.cursors import DictCursor

from mysql_config import DATABASE_CONFIG
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def singleton(cls,*args,**kw):
    instance = {}

    def _wrapper(cls):
        if cls not in instance:
            instance[cls]=cls(*args,**kw)
        return instance[cls]
    return _wrapper

@singleton
class SQLAlchemyPool(object):
    def __init__(self):
        self.__host = DATABASE_CONFIG['HOST']
        self.__user = DATABASE_CONFIG['USER']
        self.__password = DATABASE_CONFIG['PASSWORD']
        self.__database = DATABASE_CONFIG['DATABASE']
        conn_info = "mysql:"+self.__user+":"+self.__password+"@"+self.__host+"/"+self.__database
        self.__engine = create_engine(conn_info, encoding='utf-8', pool_size=20, max_overflow=0, convert_unicode=True)
        pass

    def getConnection(self):
        Session = sessionmaker()
        Session.configure(bind=self.__engine)
        session = Session()
        return session
        pass

@singleton
class MySQLPool(object):
    __instance = None

    def getSingleConnection():
        conn = MySQLdb.connect(
            DATABASE_CONFIG['HOST'],
            DATABASE_CONFIG['USER'],
            DATABASE_CONFIG['PASSWORD'],
            DATABASE_CONFIG['DATABASE'],
            charset='utf-8',
            use_unicode=True,
            cursorclass=DictCursor
        )
        wrapped_conn = MySQLConnection(conn)