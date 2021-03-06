import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


db_string = 'postgresql://postgres:admin@localhost:5432/ai-database'
db = create_engine(db_string)

Base = declarative_base()


def connect(user='postgres', password='admin', db='AI-database',
            host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    connection = sqlalchemy.create_engine(url, client_encoding='utf8')
    metadata = sqlalchemy.MetaData(bind=connection, reflect=True)
    return connection, metadata


class UserCred(Base):
    __tablename__ = 'users_credentials'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    user = relationship('User', uselist=False, back_populates="users_credetials")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey(UserCred.id))
    parent = relationship("UserCred", back_populates="users")
    user = relationship("Link", back_populates="user")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    quest = relationship("Link", back_populates="quest")


class Link(Base):
    __tablename__ = "linkage"

    userId = Column(Integer, ForeignKey(User.id), primary_key=True)
    questionId = Column(Integer, ForeignKey(Question.id), primary_key=True)

    user = relationship("User", back_populates='user')
    quest = relationship("Question", back_populates='quest')


Session = sessionmaker(db)
session = Session()


Base.metadata.create_all(db)
