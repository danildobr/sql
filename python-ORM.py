#СХЕМА БД https://github.com/netology-code/py-homeworks-db/blob/SQLPY-76/06-orm/readme/book_publishers_scheme.png
# Легенда: система хранит информацию об издателях (авторах), их книгах и фактах продажи. Книги могут продаваться в разных магазинах, поэтому требуется учитывать не только что за книга была продана, но и в каком магазине это было сделано, а также когда.
# Интуитивно необходимо выбрать подходящие типы и связи полей.

# Задание 
# Используя SQLAlchemy, составить запрос выборки магазинов, продающих целевого издателя.
# Напишите Python-скрипт, который:
# подключается к БД любого типа на ваш выбор, например, к PostgreSQL;
# импортирует необходимые модели данных;
# принимает имя или идентификатор издателя (publisher), например, через input(). Выводит построчно факты покупки книг этого издателя:

# название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки

# Пример (было введено имя автора — Пушкин):

# Капитанская дочка | Буквоед     | 600 | 09-11-2022
# Руслан и Людмила  | Буквоед     | 500 | 08-11-2022
# Капитанская дочка | Лабиринт    | 580 | 05-11-2022
# Евгений Онегин    | Книжный дом | 490 | 02-11-2022
# Капитанская дочка | Буквоед     | 600 | 26-10-2022

# createdb -U postgres bookstore_date
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import select  

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String(length=50), unique=True, nullable=False)
    
    def __str__(self):
        return f'{self.id}|{self.name}'

class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    title = sq.Column(sq.String(length=50), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id', ondelete='CASCADE'),nullable=False)

    publisher = relationship(Publisher, backref='books') 
    
    def __str__(self):
        return f'{self.id}|{self.title}|{self.id_publisher}'
        
class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String(length=50), unique=True, nullable=False)
    
    def __str__(self):
        return f'{self.id}|{self.name}'

class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id', ondelete='CASCADE'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    
    book = relationship(Book, backref='stocks') 
    shop = relationship(Shop, backref='stocks') 
    
    def __str__(self):
        return f'{self.id}|{self.id_book}|{self.id_shop}|{self.count}'
        
class Sale(Base):
    __tablename__ = 'sale' 
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    price = sq.Column(sq.Numeric(10,2), nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id', ondelete='CASCADE'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref='sales') 
    
    def __str__(self):
        return f'{self.id}|{self.price}|{self.date_sale}|{self.id_stock}|{self.count}'

def create_table(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DSN = 'postgresql://postgres:   пароль    @localhost:5432/bookstore_date' 

engine = sqlalchemy.create_engine(DSN)
create_table(engine) 

Session = sessionmaker(bind=engine)
session = Session()

publisher_1 = Publisher(name='Николай Гоголь')
publisher_2 = Publisher(name='Алексей Толстой')
publisher_3 = Publisher(name='Антон Чехов')
session.add_all([publisher_1, publisher_2, publisher_3])
session.commit()

boock_1 = Book(title='Ночь перед Рождеством', id_publisher=publisher_1.id)
boock_2 = Book(title='Вечер на хуторе близ Диканьки', id_publisher=publisher_1.id)
boock_3 = Book(title='Ревизор', id_publisher=publisher_1.id)
boock_4 = Book(title='Приключения Пиноккио', id_publisher=publisher_2.id)
boock_5 = Book(title='Белоснежка', id_publisher=publisher_2.id)
boock_6 = Book(title='Царевна-лягушка', id_publisher=publisher_2.id)
boock_7 = Book(title='Палата №6', id_publisher=publisher_3.id)
boock_8 = Book(title='Каштанка', id_publisher=publisher_3.id)
boock_9 = Book(title='Человек в футляре', id_publisher=publisher_3.id)
session.add_all([boock_1, boock_2, boock_3, boock_4, boock_5, boock_6, boock_7, boock_8, boock_9])
session.commit()

shop_1 = Shop(name='Книжный мир')
shop_2 = Shop(name='Книголюб')
shop_3 = Shop(name='Чтиво')
shop_4 = Shop(name='Букварь')
session.add_all([shop_1, shop_2, shop_3, shop_4])
session.commit()

stock_1 = Stock(id_book=boock_1.id, id_shop=shop_1.id, count=3)
stock_2 = Stock(id_book=boock_2.id, id_shop=shop_2.id, count=5)
stock_3 = Stock(id_book=boock_3.id, id_shop=shop_3.id, count=7)
stock_4 = Stock(id_book=boock_4.id, id_shop=shop_4.id, count=9)
stock_5 = Stock(id_book=boock_5.id, id_shop=shop_1.id, count=1)
stock_6 = Stock(id_book=boock_6.id, id_shop=shop_2.id, count=2)
stock_7 = Stock(id_book=boock_7.id, id_shop=shop_3.id, count=5)
stock_8 = Stock(id_book=boock_8.id, id_shop=shop_4.id, count=9)
stock_9 = Stock(id_book=boock_9.id, id_shop=shop_1.id, count=10)

session.add_all([stock_1, stock_2, stock_3, stock_4, stock_5, stock_6, stock_7, stock_8, stock_9])
session.commit()

sale_1 = Sale(price=500.50, date_sale='2023-10-05 14:30:00',id_stock=stock_1.id,count=2)
sale_2 = Sale(price=550.59, date_sale='2023-05-05 17:25:00',id_stock=stock_2.id,count=3)
sale_3 = Sale(price=699.50, date_sale='2023-07-09 10:00:00',id_stock=stock_3.id,count=4)
sale_4 = Sale(price=489.23, date_sale='2023-01-05 09:55:00',id_stock=stock_4.id,count=5)
sale_5 = Sale(price=999.50, date_sale='2023-04-15 13:15:00',id_stock=stock_5.id,count=1)
sale_6 = Sale(price=776.55, date_sale='2023-09-05 12:45:00',id_stock=stock_6.id,count=2)
sale_7 = Sale(price=399.55, date_sale='2023-08-01 09:55:00',id_stock=stock_7.id,count=3)
sale_8 = Sale(price=776.55, date_sale='2023-09-05 12:45:00',id_stock=stock_8.id,count=2)
sale_9 = Sale(price=555.55, date_sale='2023-05-05 09:30:00',id_stock=stock_9.id,count=1)

session.add_all([sale_1, sale_2, sale_3, sale_4, sale_5, sale_6, sale_7, sale_8, sale_9])
session.commit()

publisher_input = input("Введите имя или ID издателя: ")

try:
    # Пытаемся преобразовать ввод в ID
    publisher_id = int(publisher_input)
    publisher = session.query(Publisher).get(publisher_id)
except ValueError:
    # Ищем по имени
    publisher = session.query(Publisher).filter(Publisher.name.ilike(publisher_input)).first()

if not publisher:
    print(f"Издатель '{publisher_input}' не найден")
else:
    # Подзапрос для получения ID книг издателя
    book_subquery = select(Book.id).where(Book.id_publisher == publisher.id).subquery()

    # Подзапрос для получения ID стоков, связанных с книгами издателя
    stock_subquery = select(Stock.id).where(Stock.id_book.in_(book_subquery)).subquery()

    # Основной запрос для получения данных о продажах
    query = (
        session.query(
            Book.title,
            Shop.name,
            Sale.price,
            Sale.date_sale
        )
        .join(Stock, Book.id == Stock.id_book)
        .join(Shop, Stock.id_shop == Shop.id)
        .join(Sale, Stock.id == Sale.id_stock)
        .filter(Sale.id_stock.in_(stock_subquery))
        .order_by(Sale.date_sale.desc())
    )

    # Вывод результатов
    print("\nРезультаты продаж:")
    print("-" * 65)
    for title, shop, price, date in query:
        # Форматируем дату и время
        formatted_date = date.strftime('%d-%m-%Y %H:%M:%S')
        print(f"{title.ljust(35)} | {shop.ljust(15)} | {str(price).rjust(10)} | {formatted_date}")