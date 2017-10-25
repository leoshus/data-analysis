#-*- coding=utf-8 -*-

import MySQLdb
import sys
from MySQLdb.cursors import DictCursor

from database.dataEntity import TournamentInfo
from mysql_config import DATABASE_CONFIG
from sqlalchemy import create_engine, and_, or_, func, text
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
        conn_info = "mysql://"+self.__user+":"+self.__password+"@"+self.__host+"/"+self.__database
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
            # charset='utf-8',
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

if __name__ == "__main__":
    pool = SQLAlchemyPool()
    session = pool.getConnection()
    result = session.query(TournamentInfo).all()
    for res in result:
        print(res.tournamentImg)

    result = session.query(TournamentInfo).filter(TournamentInfo.gameId == 1).all()
    for res in result:
        print(res.tournamentImg)

    #fetch first data
    session.query(TournamentInfo).first()
    # session.query(TournamentInfo).filter(TournamentInfo.tournamentName == u'home').one()
    #and/or
    result = session.query(TournamentInfo).filter(and_(TournamentInfo.gameId == 1, TournamentInfo.gameId == 2)).all()
    result = session.query(TournamentInfo).filter(or_(TournamentInfo.gameId == 1, TournamentInfo.gameId == 2)).all()
    session.query(TournamentInfo).filter(TournamentInfo.gameId == 1, TournamentInfo.tournamentName == u'home').all()
    session.query(TournamentInfo).filter(TournamentInfo.gameId == 1).filter(TournamentInfo.tournamentName == u'home').all()
    #equal/like/in
    session.query(TournamentInfo).filter(TournamentInfo.gameId == 1).all()
    session.query(TournamentInfo).filter(TournamentInfo.gameId != 1).all()
    session.query(TournamentInfo).filter(TournamentInfo.gameId.in_([1, 2])).all()
    session.query(TournamentInfo).filter(~TournamentInfo.gameId.in_([1, 2])).all()
    session.query(TournamentInfo).filter(TournamentInfo.tournamentName.like(u'%home%')).all()
    print(result)
    #limit
    result = session.query(TournamentInfo).filter(TournamentInfo.gameId == 1).all()[1:3]
    session.query(TournamentInfo).order_by(TournamentInfo.createTime)
    print(result)

    #write
    tournamentInfo = TournamentInfo(tournamentName=u'home')
    session.add(tournamentInfo)
    # session.add_all([tournamentInfo, tournamentInfo])
    session.commit()
    #count
    result = session.query(TournamentInfo).filter(TournamentInfo.gameId > 1).count()
    print(result)
    session.query(func.count('*')).select_from(TournamentInfo).scalar()
    session.query(func.count(TournamentInfo.tournamentInfoId)).scalar()
    #group by
    session.query(func.count(TournamentInfo.tournamentName), TournamentInfo.tournamentName).group_by(TournamentInfo.tournamentName).all()

    #text
    session.query(TournamentInfo).filter(text("gameId>1")).all()
    session.query(TournamentInfo).filter(text("gameId>:id")).params(id=1).all()
    session.query(TournamentInfo).from_statement(text(u"select * from TournamentInfo WHERE tournamentName=:name"))\
        .params(name=u'home').all()
    #multitable query
    # session.query(A.name,B.name).filter(A.id==B.id).filter(A.xx=u'xx').all()
    #subquery
    subquery = session.query(TournamentInfo.tournamentInfoId).filter(TournamentInfo.gameId>1).subquery()
    session.query(func.count('*').label('count')).filter(TournamentInfo.tournamentInfoId.in_(subquery))
    #contains
    session.query(TournamentInfo).filter(TournamentInfo.gameId.contains([1, 2, 3]))
    #delete
    session.delete(tournamentInfo)
    pass


