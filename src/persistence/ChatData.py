from sqlalchemy import Column, String, create_engine, INT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 定义User对象:
class ChatData(Base):
    # 表的名字:
    __tablename__ = 'chat_data'

    # 表的结构:
    id = Column(INT(), primary_key=True)
    chat_id = Column(INT())

    def __init__(self, _id, name):
        self.id = _id
        self.name = name
