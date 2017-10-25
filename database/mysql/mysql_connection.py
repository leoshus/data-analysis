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

    def insertOne(self, table, *args, **kwargs):
        sql = "INSERT INTO %s" % table
        if kwargs:
            keys = tuple(kwargs.keys())
            values = tuple(kwargs.values())
            sql += "(" + ",".join(["`%s`"] * len(keys)) % keys + \
                ") VALUES (" + ",".join(["%s"] * len(values)) + ")"
        else:
            values = args
            sql += " VALUES（" + ",".join(["%s"] * len(values)) + ")"
        self.__session.execute(sql, values)
        return self.__session.lastrowid

    def insertBatch(self, table, values_list=None, *args):
        sql = "INSERT INTO %s" % table
        if args:
            keys = args
            sql += "(" + ",".join(["`%s`"] * len(keys)) % keys + ")"
            sql += " VALUES (" + ",".join(["%s"] * len(keys)) + ")"
        self.__session.executemany(sql,values_list)
        pass

    def select(self, table, where=None, fetchall=True, *args, **kwargs):
        result = None
        sql = "SELECT "
        keys = args
        values = tuple(kwargs.values())
        length = len(keys) - 1
        sql += ",".join(["`%s`"] * len(keys)) % keys + " FROM %s" % table
        if where:
            sql += " WHERE %s" % where
        # print(sql)
        self.__session.execute(sql,values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)
        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item.values()[0] for item in self.__session.fetchall()]
        if len(result) == 0:
            result = None
        else:
            if not fetchall:
                result = result[0]
        return result
        pass


if __name__ == "__main__":
    print(",".join(["`%s`"]*2))
    print(["ss"]*2)
    conn = MySQLConnection()
    conn.select("Tournament", "gameId > 1", True, 'turnamentInfoName', 'tournamentInfoImg')
