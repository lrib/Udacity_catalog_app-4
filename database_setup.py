import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """This table is for store the users."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'email': self.email,
        }


class Categoria(Base):
    """This table is for store the available categories."""
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id_cat': self.id
        }


class Item(Base):
    """This table is for store the available items."""
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(1000))
    date = Column(DateTime)
    categoria_id = Column(Integer, ForeignKey('categoria.id'))
    name_cat = relationship(Categoria)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'date': self.date,
            'categoria_id': self.categoria_id
        }


# end of code
engine = create_engine('sqlite:///project.db')

Base.metadata.create_all(engine)
