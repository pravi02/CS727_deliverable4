from sqlalchemy import Column, Integer, String, DateTime

from db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'