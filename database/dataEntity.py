#-*- coding=utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, BigInteger, DateTime, Unicode, String, Float

Base = declarative_base()


class TournamentInfo(Base):
    __tablename__ = 'TournamentInfo'
    tournamentInfoId = Column(BigInteger, primary_key=True)
    gameId = Column(BigInteger)
    tournamentImg = Column(Unicode(255))
    tournamentName = Column(Unicode(255))
    tournamentUrl = Column(Unicode(255))
    createTime = Column(DateTime)
    updateTime = Column(DateTime)
    pass



