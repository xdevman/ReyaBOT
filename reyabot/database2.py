import sqlite3

from time import time
from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

DEBUG_STATUS = False
db_name = ["dbbot.sqlite"]

dbname = db_name[0]

Base = declarative_base()
engine = create_engine(f'sqlite:///{dbname}', echo=DEBUG_STATUS)
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    userid = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    wallet_address = Column(String, default='null')
    joined = Column(BigInteger, nullable=False)
    elixir_username = Column(String, default=None) 
    rank = Column(Integer, default=None)  

Base.metadata.create_all(engine)

def add_new_user(user_id):
    new_user = User(userid=user_id, joined=int(time()))
    try:
        session.add(new_user)
        session.commit()
        return "User added successfully"
    except SQLAlchemyError as e:
        session.rollback()
        return f"Error: {e}"

def add_wallet_address(user_id, wallet_address):
    try:
        user = session.query(User).filter_by(userid=user_id).first()
        if user:
            user.wallet_address = wallet_address
            session.commit()
            return "Wallet address updated successfully"
        else:
            return "User not found"
    except SQLAlchemyError as e:
        session.rollback()
        return f"Error: {e}"

def get_wallet_address(user_id):
    try:
        user = session.query(User).filter_by(userid=user_id).first()
        if user:
            return user.wallet_address
        else:
            return "User not found"
    except SQLAlchemyError as e:
        return f"Error: {e}"

def set_elixir_username(user_id, elixir_username):
    try:
        user = session.query(User).filter_by(userid=user_id).first()
        if user:
            user.elixir_username = elixir_username
            session.commit()
            return "Elixir username updated successfully"
        else:
            return "User not found"
    except SQLAlchemyError as e:
        session.rollback()
        return f"Error: {e}"

def get_elixir_username(user_id):
    try:
        user = session.query(User).filter_by(userid=user_id).first()
        if user and user.elixir_username:
            return user.elixir_username
        else:
            return None
    except SQLAlchemyError as e:
        return f"Error: {e}"

def get_elixir_rank(user_id):
    try:
        user = session.query(User).filter_by(userid=user_id).first()
        if user and user.rank:
            return user.rank
        else:
            return None
    except SQLAlchemyError as e:
        return f"Error: {e}"
def update_user_rank(user_id, rank):
    try:
        user = session.query(User).filter_by(userid=user_id).first()
        if user:
            user.rank = rank
            session.commit()
            return "Rank updated successfully"
        else:
            return "User not found"
    except SQLAlchemyError as e:
        session.rollback()
        return f"Error: {e}"
