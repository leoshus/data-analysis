#-*- coding=utf-8 -*-


import unittest

from database.mysql.mysql_pool import MySQLPool


class TestDatabase(unittest.TestCase):

    def test_mysqlPool(self):
        print(u"test mysql pool")
        pool = MySQLPool()
        conn = pool.getConnection()
        result = conn.execute("select * from TournamentInfo")
        print(type(result))
        pass

    @unittest.skip("donot carry out")
    def test_skip(self):
        print("test skip")
        pass

if __name__ == "__main__":
    unittest.main()
