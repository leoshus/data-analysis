#-*- coding=utf-8 -*-

import MySQLdb
import sys
from MySQLdb.cursors import DictCursor

from mysql_config import DATABASE_CONFIG
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mysql_connection import MySQLConnection
from DBUtils.PooledDB import PooledDB


def singleton(cls, *args, **kw):
    instance = {}

    def _wrapper():
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
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

    def __init__(self, min_conn=2):
        self.__host = DATABASE_CONFIG['HOST']
        self.__user = DATABASE_CONFIG['USER']
        self.__password = DATABASE_CONFIG['PASSWORD']
        self.__database = DATABASE_CONFIG['DATABASE']
        self.__min_conn = min_conn
        self.__pool = PooledDB(
            MySQLdb,
            self.__min_conn,
            host=self.__host,
            user=self.__user,
            passwd=self.__password,
            db=self.__database,
            charset='utf-8',
            use_unicode=True,
            cursorclass=DictCursor
        )

    @staticmethod
    def getSingleConnection(self):
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
        return wrapped_conn
    pass

    def getConnection(self):
        try:
            conn = self.__pool.connection()
            wrapped_conn = MySQLConnection(conn)
            return wrapped_conn
        except MySQLdb.Error as e:
            sys.stderr.write("Error %d:%s\n" % (e.args[0], e.args[1]))
            return None
    pass
