from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship('Book', back_populates='publisher', uselist=True)


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    id_publisher = Column(Integer, ForeignKey('publishers.id'))

    publisher = relationship('Publisher', back_populates='books')
    stocks = relationship('Stock', back_populates='book', uselist=True)


class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('books.id'))
    id_shop = Column(Integer, ForeignKey('shops.id'))
    count = Column(Integer, nullable=False)

    book = relationship('Book', back_populates='stocks')
    sales = relationship('Sale', back_populates='stock', uselist=True)


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    date_sale = Column(DateTime, nullable=False)
    id_stock = Column(Integer, ForeignKey('stocks.id'))
    count = Column(Integer, nullable=False)

    stock = relationship('Stock', back_populates='sales')
