from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean, Text, Float, JSON
from sqlalchemy.orm import Relationship
from sqlalchemy.orm import declarative_base

from database.connect import session

Base = declarative_base()
Base.query = session.query_property()


class Model(Base):

    __abstract__ = True

    @classmethod
    def filter_id(cls, table_id):
        try:
            return cls.query.filter(cls.id == table_id).first()
        except AttributeError as e:
            raise AttributeError(f"{cls} doesn't attribute id")


class TimeStampedModel(Model):

    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())


class User(TimeStampedModel):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    nickname = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    analyses = Relationship('Analysis', back_populates='user', uselist=True, passive_deletes=True)

    def __repr__(self):
        if self.preference:
            return f'User({self.preference.name}; id: {self.preference.id})'
        else:
            return super().__repr__()

    @classmethod
    def verify_login(cls, email, password):
        try:
            return cls.query.filter(cls.email == email).filter(cls.password == password).first()
        except KeyboardInterrupt as e:
            raise KeyboardInterrupt
        except Exception as e:
            return None


# class Song(TimeStampedModel):
#
#     __tablename__ = 'songs'
#
#     id = Column(Integer, primary_key=True)
#
#     name = Column(Text)
#     genre = Column(Text)
#
#     album = Column(Text)
#     composer = Column(Text)
#     lyric_writer = Column(Text)
#
#     lyrics = Column(Text)
#     lyrics_row = Column(Integer)
#
#     year = Column(Integer)
#     month = Column(Integer)
#     day = Column(Integer)
#
#     ranks = Relationship('Rank', back_populates='song', uselist=True, passive_deletes=True)
#     analyses = Relationship('Analysis', back_populates='song', uselist=True, passive_deletes=True)
#
#
# class Rank(TimeStampedModel):
#
#     __tablename__ = 'ranks'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     date = Column(Date)
#     rank = Column(Integer)
#
#     song_id = Column(Integer, ForeignKey('songs.id', ondelete='CASCADE'), nullable=True, index=True)
#     song = Relationship('Song', back_populates='ranks')


# class Analysis(TimeStampedModel):
#
#     __tablename__ = 'analyses'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50))
#     setting = Column(JSON)
#     result_song = Column(JSON)
#     result_cluster = Column(JSON)
#
#     user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
#     user = Relationship('User', back_populates='analyses')
