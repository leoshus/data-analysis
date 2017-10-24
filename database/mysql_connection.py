#-*- coding=utf-8 -*-

import traceback


class MySQLConnection(object):

    def __init__(self, conn):
        self.__conn = conn
        self.__session = self.__conn.cursor()
        pass

    def close(self):
        try:
            self.__session.close()
            self.__conn.close()
        except:
            traceback.print_exc()
        pass

    def execute(self, sql):
        self.__session.execute(sql)
        ret = self.__session.fetchall()
        return ret


    def beginTransaction(self):
        self.__conn.autocommit(0)
        pass

    def endTransaction(self, option='commit'):
        if option == 'commit':
            self.__conn.commit()
        else:
            self.__conn.rollback()
        pass

