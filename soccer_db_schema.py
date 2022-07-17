from sqlite3 import Timestamp
from sqlalchemy import (
    TIME,
    BigInteger,
    Column,
    Float,
    ForeignKey,
    Index,
    Integer,
    TIMESTAMP,
    String,
    ForeignKey,
    Table,
    func,
    Boolean,
    false,
    true,
    and_,
    DATETIME
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
import requests
from sqlalchemy.sql.expression import distinct
from sqlalchemy.sql.sqltypes import DATE, DateTime
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import select, case
from sqlalchemy import func

Base = declarative_base()
metadata = Base.metadata

class LK_Play_Type(Base):
    __tablename__='lk_play_types'

    id=Column(Integer,primary_key=True,autoincrement=False)
    name = Column(String)

class LK_Play_Pattern(Base):
    __tablename__='lk_play_patterns'

    id=Column(Integer,primary_key=True,autoincrement=False)
    name = Column(String)

class LK_Attribute(Base):
    __tablename__='lk_attributes'

    id=Column(Integer,primary_key=True,autoincrement=False)
    name = Column(String)

class LK_Position(Base):
    __tablename__='lk_positions'

    id=Column(Integer,primary_key=True,autoincrement=False)
    name = Column(String)

class Team(Base):
    __tablename__='teams'

    id=Column(Integer,primary_key=True,autoincrement=False)
    name = Column(String)

class Player(Base):
    __tablename__='players'

    id=Column(Integer,primary_key=True,autoincrement=False)
    name = Column(String)
    team_id = Column(Integer,ForeignKey('teams.id'))
    jersey_number = Column(Integer)


class Game(Base):
    __tablename__='games'

    match_id=Column(Integer,primary_key=True,autoincrement=False)
    match_date = Column(DATE)
    home_team_id = Column(Integer,ForeignKey('teams.id'))
    away_team_id = Column(Integer,ForeignKey('teams.id'))
    home_team = relationship('Team',foreign_keys=[home_team_id],uselist=False)
    away_team = relationship('Team',foreign_keys=[away_team_id],uselist=False)
    home_score=Column(Integer)
    away_score=Column(Integer)


class Event(Base):
    __tablename__='events'

    id=Column(String,primary_key=True,autoincrement=False)
    match_id = Column(Integer,ForeignKey('games.match_id'))
    index=Column(Integer)
    period=Column(Integer)
    possession_number = Column(Integer)
    timestamp = Column(TIME)
    type_id = Column(Integer,ForeignKey('lk_play_types.id'))
    player_id = Column(Integer,ForeignKey('players.id'))
    position_id = Column(Integer,ForeignKey('lk_positions.id'))
    team_id = Column(Integer,ForeignKey('teams.id'))
    possession_team_id = Column(Integer,ForeignKey('teams.id'))
    location_x = Column(Float)
    location_y = Column(Float)
    under_pressure = Column(Boolean,server_default=false(), default=False)
    end_location_x = Column(Float)
    end_location_y = Column(Float)
    end_location_z = Column(Float)
    duration=Column(Float)
    recieve_player_id = Column(Integer,ForeignKey('players.id'))
    cross = Column(Boolean,server_default=false(), default=False)
    switch = Column(Boolean,server_default=false(), default=False)
    outcome_id = Column(Integer,ForeignKey('lk_attributes.id'))
    pass_type_id = Column(Integer,ForeignKey('lk_attributes.id'))
    has_360 = Column(Boolean,server_default=false(), default=False)

