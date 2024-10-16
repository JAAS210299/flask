from sqlalchemy import Boolean, Column, ForeignKey, DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Categorias(db.Model):
    """"Categorias de los articulos"""
    __tablename__ = 'categorias'
    id =  Column(Integer, primary_key=True)
    nombre = Column(String(100))
    articulos = relationship("Articulos", cascade="all, delete-orphan", backref="Categorias", lazy='dynamic')
    def __repr__(self):
        return (u'<{sel.__class__.__name__}: {sel.id}>)'.format(self=self))
    
class Articulos(db.Model):
    """Articulos de nuestra tienda"""
    __tablename__ = 'articulos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=True)
    precio = Column(Float,default=0)
    iva = Column(Integer, default=21)
    descripcion = Column(String(255))
    image = Column(String(255))
    stock = Column(Integer,default=0)
    CategoriaId = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    categoria = relationship("Categorias", backref="Articulos")
    def precio_final(self):
        return self.precio+(self.precio*self.iva/100)
    def __repr__(self):
        return (u'<{self.__class__.name__}: {self.id}>'.format(self=self))
