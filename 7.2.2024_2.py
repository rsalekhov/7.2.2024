import json
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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


def create_tables(engine):
    Base.metadata.create_all(engine)


def insert_test_data(session, json_url):
    with open(json_url, 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def get_shops_by_publisher(session, publisher_input):
    try:
        publisher_id = int(publisher_input)
        publisher = session.query(Publisher).filter_by(id=publisher_id).first()
    except ValueError:
        publisher = session.query(Publisher).filter_by(name=publisher_input).first()

    if publisher:
        for book in publisher.books:
            for stock in book.stocks:
                shop = session.query(Shop).filter_by(id=stock.id_shop).first()
                sale = session.query(Sale).filter_by(id_stock=stock.id).first()

                if shop and sale:
                    print(f"{book.title} | {shop.name} | {sale.price} | {sale.date_sale.strftime('%d-%m-%Y')}")
    else:
        print("Издатель не найден.")


if __name__ == "__main__":
    DSN = '...'  # Ваш DSN (Data Source Name) для подключения к БД
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    json_url = 'https://raw.githubusercontent.com/netology-code/py-homeworks-db/SQLPY-76/06-orm/fixtures/tests_data.json'
    insert_test_data(session, json_url)

    publisher_name = input("Введите имя издателя или его идентификатор: ")
    get_shops_by_publisher(session, publisher_name)
