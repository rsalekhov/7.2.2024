import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale


DSN = '...'

engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()


def get_shops_by_publisher(publisher_name):
    publisher = session.query(Publisher).filter_by(name=publisher_name).first()

    if publisher:
        books = publisher.books
        for book in books:
            for stock in book.stocks:
                shop = session.query(Shop).filter_by(id=stock.id_shop).first()
                sale = session.query(Sale).filter_by(id_stock=stock.id).first()

                if shop and sale:
                    print(f"{book.title} | {shop.name} | {sale.price} | {sale.date_sale.strftime('%d-%m-%Y')}")


if __name__ == "__main__":
    publisher_name = input("Введите имя издателя: ")
    get_shops_by_publisher(publisher_name)
